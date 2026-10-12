# opencode-skills

57 OpenCode skills vendored from [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) (`dev` branch, Oct 2026), installed for global use.

## Layout

Each directory is one skill (`<id>/SKILL.md` + supporting files):

| Group | Skills |
| --- | --- |
| Core workflow (shared) | `ast-grep`, `browser`, `coding-agent-sessions`, `data-scientist`, `debugging`, `frontend`, `git-master`, `init-deep`, `lsp-setup`, `programming`, `refactor`, `remove-ai-slops`, `review-work`, `ultimate-browsing`, `ulw-execute`, `ulw-plan`, `ulw-research`, `visual-qa` |
| Senpi-native | `dag-library`, `give-me-tips`, `mass-ulw`, `onboarding`, `ultrawork`, `ulw-loop`, `visualize`, `senpi-hyperplan`, `senpi-init-deep`, `senpi-ulw-plan`, `senpi-ulw-research` |
| Codex components | `comment-checker`, `lcx-contribute-bug-fix`, `lcx-doctor`, `lcx-report-bug`, `lsp`, `rules`, `teammode`, `codex-ulw-plan`, `codex-ulw-loop` |
| Dev/QA | `codex-qa`, `get-unpublished-changes`, `github-triage`, `omomomo`, `opencode-qa`, `publish`, `remove-deadcode`, `senpi-qa`, `tech-debt-audit`, `work-with-pr`, `pre-publish-review`, `agents-security-research`, `agents-hyperplan`, `opencode-hyperplan` |
| Built-in variants | `dev-browser`, `builtin-frontend`, `builtin-git-master`, `builtin-security-research` |
| Misc | `x-search` |

Overlapping upstream variants are namespaced (`senpi-*`, `codex-*`, `agents-*`, `opencode-*`, `builtin-*`); the shared/OpenCode edition keeps the canonical ID.

## Install

```sh
cp -r <id> ~/.config/opencode/skills/<id>
```

## Known asset gaps (upstream limits, not install defects)

- `frontend` third-party upstreams are empty (GitHub tarballs exclude submodule contents).
- `browser` omowright runtime is unstaged (needs `npm`/`bun` at build time).
- `*.mjs` helper scripts need `node`/`bun` to execute.

## Provenance

Source: `https://github.com/code-yeongyu/oh-my-openagent` @ `dev`, October 2026.
Identical `.opencode/skills/{github-triage,pre-publish-review,work-with-pr}` duplicates of `.agents/skills` were deduplicated.
`builtin-security-research/SKILL.md` gained a `description` frontmatter (upstream file had none, so OpenCode would not advertise it).
