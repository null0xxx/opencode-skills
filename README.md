# opencode-skills

The complete global OpenCode V2 setup for this account, exactly as installed on the
author's machine: **57 skills + 57 slash commands + global config files**.

## Layout

| Path | Contents |
| --- | --- |
| `skills/` | 57 skill directories (`<id>/SKILL.md` plus supporting scripts and references) |
| `commands/` | 57 command files (`<id>.md`, one per skill) |
| `config/opencode.json` | Global OpenCode config (skills path, subagents, provider, permissions) |
| `config/AGENTS.md` | Global instructions file |
| `INSTALL-PROMPT.md` | Ready-to-paste prompt that installs this setup, verbatim, on another machine |
| `docs/VENDORING.md` | Provenance of the vendored upstream skill pack |

Every installed `SKILL.md` carries an `## Installed OpenCode v2 compatibility`
section so the vendored workflows run correctly on OpenCode V2.

## Install on another machine

Copy the content of `INSTALL-PROMPT.md` into an OpenCode agent on the target
machine and let it run. It:

1. verifies/installs OpenCode V2,
2. clones (or downloads) this repo,
3. copies `skills/`, `commands/` and `config/` into `~/.config/opencode/`,
4. substitutes the `/home/secc` home path with the target machine's home,
5. verifies the result (57 skills, 57 commands, 57 compatibility sections).

## Manual install (Linux/macOS)

```sh
git clone https://github.com/null0xxx/opencode-skills /tmp/opencode-skills
mkdir -p ~/.config/opencode
cp -a /tmp/opencode-skills/skills/. ~/.config/opencode/skills/
cp -a /tmp/opencode-skills/commands/. ~/.config/opencode/commands/
cp /tmp/opencode-skills/config/opencode.json ~/.config/opencode/opencode.json
cp /tmp/opencode-skills/config/AGENTS.md ~/.config/opencode/AGENTS.md
```

Then replace `/home/secc` with your home directory inside the copied files.

## Windows

Target directory: `%USERPROFILE%\.config\opencode`. See `INSTALL-PROMPT.md`.
`skills/ast-grep/bin/sg` (the ~51 MB Linux binary) is intentionally **not**
vendored; on Windows run `skills\ast-grep\install.ps1` to install `sg.exe`.

## Intentionally not in this repo

- `skills/ast-grep/bin/sg` — 51 MB platform binary (use the skill's `install.sh` / `install.ps1`).
- `__pycache__` directories — regenerable Python bytecode caches.
- `service.json` — machine-generated local server password (OpenCode recreates it).
- `~/.local/share/opencode-skill-runtimes/` — 178 MB generated runtime data, not config.

## Updating

```sh
cd ~/.local/share/opencode-skills   # or wherever you cloned it
git pull
# then re-copy skills/ and commands/ to ~/.config/opencode/ if anything changed
```
