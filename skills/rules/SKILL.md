---
name: rules
description: Use when the user asks about Codex Rules behavior, injected project rules, supported rule file locations, matching, or environment configuration.
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

# Codex Rules

Codex Rules is automatic once the plugin is enabled. It injects:

- static project instructions on `SessionStart` and `UserPromptSubmit`
- matching file-specific rules after Codex `apply_patch` by default

Dynamic `PostToolUse` output is injected as additional context and is deduplicated per plugin data session. Codex Rules does not rewrite tool output.

Supported project sources:

- `CONTEXT.md`
- `.omo/rules/**/*.md`
- `.claude/rules/**/*.md`
- `.cursor/rules/**/*.md`
- `.github/instructions/**/*.md`
- `.github/copilot-instructions.md`

Supported environment knobs:

- `CODEX_RULES_DISABLED=1`
- `CODEX_RULES_MODE=both|static|dynamic|off`
- `CODEX_RULES_MAX_RULE_CHARS=<number>`
- `CODEX_RULES_MAX_RESULT_CHARS=<number>`
- `CODEX_RULES_ENABLED_SOURCES=CONTEXT.md,.omo/rules`

The legacy `PI_RULES_*` variables are accepted as fallbacks for users migrating from `pi-rules`.
