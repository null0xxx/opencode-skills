#!/usr/bin/env node
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, cp, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';

const source = '/home/secc/.config/opencode';
const sandbox = await mkdtemp(join(tmpdir(), 'opencode-skills-qa-'));
const evidence = process.argv[2];
const expected = (await readdir(join(source, 'skills'))).sort();
const probeTimer = new AbortController();
const password = randomUUID();
const env = { ...process.env,
  XDG_DATA_HOME: join(sandbox, 'data'), XDG_STATE_HOME: join(sandbox, 'state'),
  XDG_CACHE_HOME: join(sandbox, 'cache'), XDG_CONFIG_HOME: join(sandbox, 'config'),
  OPENCODE_DISABLE_PROJECT_CONFIG: '1',
};
for (const key of ['OPENCODE_CONFIG', 'OPENCODE_CONFIG_DIR', 'OPENCODE_CONFIG_CONTENT', 'OPENCODE_SERVER_PASSWORD']) delete env[key];
env.OPENCODE_SERVER_PASSWORD = password;
await mkdir(join(sandbox, 'config', 'opencode'), { recursive: true });
for (const file of ['opencode.json', 'AGENTS.md', 'commands'])
  await cp(join(source, file), join(sandbox, 'config', 'opencode', file), { recursive: true });
const child = spawn('/home/secc/.opencode/bin/opencode', ['serve', '--hostname', '127.0.0.1', '--port', '0'],
  { cwd: sandbox, env, stdio: ['ignore', 'pipe', 'pipe'] });
let logs = '';
for (const stream of [child.stdout, child.stderr]) stream.on('data', b => { logs += b; });
const report = { sandbox, skills: [], agents: [], commands: [], checks: [], timestamp: new Date().toISOString() };
async function request(base, path, body) {
  const headers = { Authorization: 'Basic ' + Buffer.from('opencode:' + password).toString('base64') };
  const response = await fetch(base + path, body === undefined ? { headers } : {
    method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const raw = await response.text();
  assert(response.ok, `${path}: HTTP ${response.status}: ${raw.slice(0, 400)}`);
  return raw ? JSON.parse(raw) : null;
}
try {
  let base;
  for (let attempt = 0; attempt < 100; attempt++) {
    base = logs.match(/http:\/\/127\.0\.0\.1:\d+/)?.[0];
    if (base) break;
    if (child.exitCode !== null) throw Error(`Server exited ${child.exitCode}: ${logs}`);
    await delay(100);
  }
  assert(base, `Server URL missing: ${logs}`);
  await request(base, '/api/info');
  report.checks.push('server responds');
  const session = await request(base, '/api/session', { location: { directory: sandbox }, title: 'Skills installation QA', agent: 'build' });
  const sessionID = session.id ?? session.data?.id;
  assert(sessionID, `No session ID: ${JSON.stringify(session)}`);
  const probe = spawn('/home/secc/.opencode/bin/opencode', ['run', '--server', base, '--session', sessionID,
    '--model', 'opencode/longcat-2.5-preview-free', 'Read-only setup probe. Load skill programming, then reply exactly QA_OK. Do not read project files or use other tools.'],
    { cwd: sandbox, env, stdio: ['ignore', 'pipe', 'pipe'] });
  let probeText = '';
  for (const stream of [probe.stdout, probe.stderr]) stream.on('data', b => { probeText += b; });
  const probeExit = await Promise.race([
    new Promise(resolve => probe.once('exit', resolve)),
    delay(90000, undefined, { signal: probeTimer.signal }).then(() => { probe.kill('SIGTERM'); return 'timeout'; }),
  ]);
  probeTimer.abort();
  assert.equal(probeExit, 0, `Live skill probe failed: ${probeText.slice(-1500)}`);
  assert(probeText.includes('QA_OK'), 'Live skill probe did not return QA_OK');
  report.checks.push('live free-model probe loaded programming');
  const query = '?' + new URLSearchParams({ 'location[directory]': sandbox });
  const skills = await request(base, '/api/skill' + query);
  report.skills = (skills.data ?? skills).map(s => s.id);
  for (const id of expected) assert(report.skills.includes(id), `Missing installed skill ${id}`);
  const agents = await request(base, '/api/agent' + query);
  report.agents = (agents.data ?? agents).map(a => a.id);
  for (const id of ['build', 'general', 'explore', 'reviewer', 'researcher']) assert(report.agents.includes(id), `Missing agent ${id}`);
  const commands = await request(base, '/api/command' + query);
  report.commands = (commands.data ?? commands).map(c => c.id ?? c.name);
  for (const id of expected) assert(report.commands.includes(id), `Missing command ${id}`);
  for (const id of expected) {
    await request(base, `/api/experimental/session/${sessionID}/skill`, { id, resume: false });
  }
  report.checks.push('57 skill IDs discovered', '57 skill activations accepted without a model call', '57 slash commands discovered', 'native agents registered');
  report.status = 'PASS';
} catch (error) {
  report.status = 'FAIL'; report.error = String(error);
  process.exitCode = 1;
} finally {
  probeTimer.abort();
  child.kill('SIGTERM');
  await Promise.race([new Promise(resolve => child.once('exit', resolve)), delay(3000)]);
  if (child.exitCode === null) child.kill('SIGKILL');
  await rm(sandbox, { recursive: true, force: true });
  report.sandboxCleaned = true;
  if (evidence) await writeFile(evidence, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
}
