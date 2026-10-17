---
name: get-unpublished-changes
description: "Compare HEAD with the latest published npm versions and list all unpublished changes by release layer. Triggers: unpublished changes, changelog, what changed, whats new."
disable-model-invocation: true
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

IMMEDIATELY output the analysis. NO questions. NO preamble.

## CRITICAL: DO NOT just copy commit messages!

For each commit, you MUST:
1. Read the actual diff to understand WHAT CHANGED
2. Describe the REAL change in plain language
3. Explain WHY it matters (if not obvious)

## Release Layers

Analyze every change against these exact layers:

| Layer | Includes | Version question |
|---|---|---|
| `omo pure components` | `packages/*-core`, MCP packages, `packages/shared-skills`, reusable scripts | Do shared components need a patch/minor/major release note even if adapters only consume them internally? |
| `omo opencode` | Root `oh-my-opencode` / `oh-my-openagent`, `src/`, `.opencode/`, `.agents/`, CLI, config, hooks, tools, docs | What semver bump should the OpenCode/OpenAgent npm packages use? |
| `omo codex` | `packages/omo-codex`, `lazycodex-ai`, Codex plugin metadata/hooks, bundled MCP runtimes, `code-yeongyu/lazycodex` marketplace payload | Does LazyCodex need the same bump, a Codex-only note, or a marketplace release? |

Exclude commits and paths matching `senpi`, `omo-senpi`, `senpi-task`, `pi-goal`, or `pi-webfetch` from user-facing notes and version recommendations. Record them only in a separate internal-adapter exclusion ledger.

## Steps:
1. Detect latest published versions for `oh-my-opencode`, `oh-my-openagent`, and `lazycodex-ai`.
2. Run `git diff v{published-version}..HEAD` to see actual changes.
3. Classify every file into one or more release layers before grouping by feat/fix/refactor/docs.
4. Describe the REAL changes and why each layer cares.
5. Note breaking changes by affected layer.
6. Recommend a layer-specific version bump and one overall workflow bump.

## Output Format:
- feat: "Added X that does Y" (not just "add X feature")
- fix: "Fixed bug where X happened, now Y" (not just "fix X bug")
- refactor: "Changed X from A to B, now supports C" (not just "rename X")

Include:
- `Layered Impact Matrix`: rows for `omo pure components`, `omo opencode`, `omo codex`
- `Layer-specific Version Recommendation`: patch/minor/major per layer plus one overall release bump
