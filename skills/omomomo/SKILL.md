---
name: omomomo
description: "Easter egg command - about oh-my-opencode. Triggers: omomomo, about, easter egg."
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

You found an easter egg! 🥚✨

Print the following message to the user EXACTLY as written (in a friendly, celebratory tone):

---

# 🎉 oMoMoMoMoMo···

**You found the easter egg!** 🥚✨

## What is Oh My OpenCode?

**Oh My OpenCode** is a powerful OpenCode plugin that transforms your AI agent into a full development team:

- 🤖 **Multi-Agent Orchestration**: Oracle (GPT-5.6 Sol), Librarian & Explore (GPT 5.6 Luna Fast), Frontend Engineer (Gemini), and more
- 🔧 **LSP Tools**: Full IDE capabilities for your agents - hover, goto definition, find references, rename, code actions
- 🔍 **AST-Grep**: Structural code search and replace across 25 languages
- 📚 **Built-in MCPs**: Context7 for docs, Exa for web search, grep.app for GitHub code search
- 🔄 **Background Agents**: Run multiple agents in parallel like a real dev team
- 🎯 **Claude Code Compatibility**: Your existing Claude Code config just works

## Who Made This?

Created with ❤️ by **[code-yeongyu](https://github.com/code-yeongyu)**

🔗 **GitHub**: https://github.com/code-yeongyu/oh-my-opencode

---

*Enjoy coding on steroids!* 🚀
