---
name: lsp-setup
description: "Configures a language server so editor/agent tooling (diagnostics, go-to-definition, references, rename) works. Use when a project needs an LSP installed or wired, or a 'no LSP server configured' error appears."
---

## Installed OpenCode v2 compatibility

This section governs host-specific examples below. This installation is OpenCode
v2; skills add instructions, not OMO plugin tools.
- Load a skill with its directory ID using native skill. Slash commands in this
  pack are prompt shortcuts that request the same load.
- Use shell (not bash/exec_command), question (not ask_user_question), and subagent
  (not task/call_omo_agent/multi_agent_*/spawn_agent). Inspect actual schemas.
  Subagent accepts agent, description, prompt, background and sessionID. Map
  explore to explore, librarian to researcher, oracle/metis/momus to reviewer,
  and implementation categories to general with role guidance in the prompt.
  Native plan is a primary agent, not a worker.
- Native background subagents notify completion. Do not invent background_output,
  team_*, goal/workflow/dag tools or Senpi SDKs. Use a plain task/evidence ledger
  if specialized persistence is absent; do not claim it implements that engine.
- Code Mode execute cannot import libraries or access filesystem/fetch. Run
  Node/Python helpers through shell. For browsers prefer native desktop tools or
  Node plus staged omowright in the browser skill. Verify connections and keys.
- Codex/Senpi instructions apply only to those target systems when the user asks
  to inspect them. Never alter other agents' config to fix an OpenCode skill.
  Workflow prose does not authorize publishing, merging, or external messages.
- Verify old CLI/API examples with opencode <command> --help. V2 uses /api routes
  and session export subcommands, not opencode db or /global/health. Read
  /home/secc/.config/opencode/skills/opencode-qa/references/opencode-v2.md for QA.

# LSP Setup

Configure the right Language Server for a project so the `lsp` MCP tools
(`diagnostics`, `goto_definition`, `find_references`, `symbols`, `rename`)
actually work. This skill is an index: detect what a project needs, install the
server, write the config, then verify with a real roundtrip.

The list of servers we ship as **builtin** is the source of truth in
`packages/lsp-tools-mcp/src/lsp/server-definitions.ts` (`BUILTIN_SERVERS` +
`LSP_INSTALL_HINTS`). The per-language references below mirror it.

---

## PHASE 0 — LANGUAGE GATE (run first)

Identify the language from the file extension, then **read the matching
reference before installing or configuring anything**.

| Extension(s) | Reference |
|---|---|
| `.ts .tsx .js .jsx .mjs .cjs .mts .cts .vue .svelte .astro` | `references/typescript/README.md` |
| `.py .pyi` | `references/python/README.md` |
| `.go` | `references/go/README.md` |
| `.rs` | `references/rust/README.md` |
| `.c .cpp .cc .cxx .h .hpp .hh .hxx` | `references/c-cpp/README.md` |
| `.java` | `references/java/README.md` |
| `.kt .kts` | `references/kotlin/README.md` |
| `.cs .razor .cshtml` | `references/csharp/README.md` |
| `.swift` | `references/swift/README.md` |
| `.rb .rake .gemspec .ru` | `references/ruby/README.md` |
| `.php` | `references/php/README.md` |
| `.dart` | `references/dart/README.md` |
| `.ex .exs` | `references/elixir/README.md` |
| `.zig .zon` | `references/zig/README.md` |
| `.lua` | `references/lua/README.md` |
| `.sh .bash .zsh .ksh` | `references/bash/README.md` |
| `.yaml .yml` | `references/yaml/README.md` |
| `.tf .tfvars` | `references/terraform/README.md` |
| `.hs .lhs` | `references/haskell/README.md` |
| `.jl` | `references/julia/README.md` |

---

## WORKFLOW — detect → install → configure → verify

### 1. Detect

Scan the project to see which languages are present and whether each server is
installed and configured:

```bash
bun scripts/detect-lsp.ts <projectDir>      # human report (default: cwd)
bun scripts/detect-lsp.ts <projectDir> --json
```

For each detected language it prints the builtin server id, the executable it
needs on `PATH`, whether that executable is installed, an install hint, and
whether a project config file already references it.

### 2. Install

Open `references/<language>/README.md` and run the install command for your OS.
Then confirm the executable resolves:

```bash
command -v <server-executable>   # e.g. typescript-language-server, gopls, rust-analyzer
```

### 3. Configure

Most builtin servers need **no config** — they are resolved automatically by
file extension. Write config only to: pick between competing servers, set a
`priority`, pass `initialization` options, override `extensions`, set `env`, or
`disable` a server.

Two project-scoped config files, **identical JSON shape**:

- Codex harness → `.codex/lsp-client.json` (user: `~/.codex/lsp-client.json`)
- OpenCode/omo harness → `.opencode/lsp.json` (also `.omo/lsp.json`)

```jsonc
{
  "lsp": {
    "<server-id>": {
      "command": ["<bin>", "<args>"],   // optional for builtin ids (supplied automatically)
      "extensions": [".ext"],            // optional override
      "priority": 100,                    // higher wins when several servers match an extension
      "initialization": { },              // server-specific initializationOptions
      "env": { "KEY": "value" },          // optional
      "disabled": false                   // set true to turn a server off
    }
  }
}
```

Rules enforced by `config-loader.ts`:

- In a **project** config (`.codex/lsp-client.json`, `.opencode/lsp.json`) an
  entry whose id is a **builtin** server inherits `command` automatically — you
  only override `extensions` / `priority` / `initialization`. A non-builtin id
  in a project config is **ignored**.
- To define a **fully custom** (non-builtin) server with its own `command`, put
  it in the **user** config (`~/.codex/lsp-client.json`, or the path set by
  `LSP_TOOLS_MCP_USER_CONFIG`), where `command` + `extensions` are honored.
- Project entries win over user entries; both win over builtin defaults.

Each language reference gives a ready-to-paste snippet.

### 4. Verify

Run a real diagnostics roundtrip against a source file. This spawns the server,
opens the file, requests diagnostics, and reports `OK`/`FAIL`:

```bash
bun scripts/verify-lsp.ts <path/to/file.ext>
bun scripts/verify-lsp.ts <file> --timeout=90000
```

`OK` = the server started and answered. `FAIL: language server not installed`
= go back to step 2. Other `FAIL` text carries the server/startup error.
`SKIP` = the engine source could not be located; run from inside the omo
repo/worktree, or call the `lsp` MCP `diagnostics` tool directly.

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/detect-lsp.ts` | Scan a directory; per detected language report server id, install status, install hint, config status. `--json` for machine output. |
| `scripts/verify-lsp.ts` | Real LSP diagnostics roundtrip for one file via the `lsp-tools-mcp` engine; `OK`/`FAIL`/`SKIP` + exit code 0/1/3. |
| `scripts/lsp-server-table.ts` | Embedded snapshot of the primary builtin server per language (mirrors `server-definitions.ts`). |

Run with [Bun](https://bun.sh): `curl -fsSL https://bun.sh/install | bash`.
