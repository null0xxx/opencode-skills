---
name: comment-checker
description: Use when Codex needs to understand or respond to automatic comment-checker feedback emitted after an edit-like PostToolUse hook.
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

# Codex Comment Checker

The plugin registers a `PostToolUse` hook for successful `apply_patch`, `write`, `edit`, `multi_edit`, and `multiedit` calls.

When comment-checker reports a warning after a patch, Codex receives blocking feedback and should fix or explain the flagged comment before moving on.

## Scope

- No MCP tool is exposed.
- Non-edit tools are ignored by this plugin.
- Missing checker binaries emit no hook output so normal Codex work can continue.
