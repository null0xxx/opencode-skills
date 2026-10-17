# OpenCode v2 local QA

This machine uses OpenCode 2.0.27. The old v1 shell scripts are retained as
reference fixtures, not the v2 verification entry point. Run
`node scripts/v2-smoke.mjs` from this skill directory for isolated v2 discovery,
agent registration, command registration and skill-loading verification.

Check flags with `opencode <command> --help`. Known v2 entry points:

- `opencode run --standalone --model opencode/longcat-2.5-preview-free --format json "<prompt>"`
- `opencode api skill.list --param 'location.directory=<workspace>'`
- `opencode api agent.list --param 'location.directory=<workspace>'`
- `opencode api command.list --param 'location.directory=<workspace>'`
- `opencode session export <session-id> --sanitize`
- `opencode serve --hostname 127.0.0.1 --port 0`

V2 HTTP routes are `/api/info`, `/api/skill`, `/api/agent`, `/api/command`,
`/api/session`, and `/api/event`. Location uses deep-object query parameters
`location[directory]`, not the v1 `directory` parameter. A location's catalogs
may be lazy: initialize a session before treating an empty listing as proof
that installation failed. Use the published v2 OpenAPI schema to check shapes:
https://dev.opencode.ai/v2/openapi.json.

For tests isolate `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME` using a
fresh temporary directory. Use a fresh `XDG_CONFIG_HOME` and copy the installed
config, AGENTS.md, commands and skills into it. Do not repurpose HOME; do not
copy credentials. No real project files should be sent to a model for a smoke
test. Prefer API skill activation to a paid model call for bulk discovery.

Read-only DB investigations use Python sqlite3 URI `mode=ro`, after obtaining
the DB path from `opencode debug paths`. Inspect sqlite_master and table_info
first: v2 uses different tables, so never run old v1 queries blindly.
