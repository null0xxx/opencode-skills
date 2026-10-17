# OpenCode skills workflow

This is OpenCode v2. Skills are installed under `/home/secc/.config/opencode/skills`.
Load applicable skills with the native `skill` tool and their directory ID. Read the
routed references before using them. Prefer canonical skills over `builtin-*`,
`codex-*`, `senpi-*`, and `agents-*` variants. A skill adds instructions, not tools.

Use `programming` for code, `debugging` for a reproducible defect, `frontend` and
`visual-qa` for UI, `git-master` for Git changes, and `review-work` for substantial
implementation review. Load `ulw-plan`, `ulw-execute`, and `ulw-research` when the
user requests those workflows. Keep skill selection specific to the actual task.

The OpenCode v2 compatibility section in each installed skill governs host/tool
differences. V2 uses `shell`, `subagent`, `question`, `skill`, and `execute`; it does
not expose Codex `multi_agent_*`, Senpi `workflow`/`dag`, or the legacy OMO `task`
category API. Inspect actual tool schemas instead of inventing tools or arguments.
For workers use `general`, exploration `explore`, research `researcher`, and review
`reviewer`. Background subagents notify completion; continue using their sessionID.
Do not interpret the presence of a skill as authorization to publish or merge.

V2 Code Mode `execute` cannot import libraries or access the filesystem directly.
Run skill-owned Node/Python scripts through `shell`. Use the native desktop browser
tools when available, or the staged omowright runtime with Node in a task-owned
browser profile for unsigned-in QA. Signed-in browsing requires a connected user
browser; never clone or modify the live profile to work around a missing connection.

Follow the user's scope and project AGENTS.md. Inspect before editing, preserve
unrelated changes, and verify the actual resulting behavior with evidence before
claiming completion. If an optional paid service, API key, browser connection, or
host-only capability is missing, say which part is unavailable and continue the
independent work. Do not report an unavailable gate as passed.

GitHub CLI is authenticated as `null0xxx`. Use that existing connection for
authorized GitHub work without printing credentials. Answer in Georgian unless
the user requests another language.
