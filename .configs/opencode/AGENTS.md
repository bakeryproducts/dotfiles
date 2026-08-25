# Global Agent Instructions

# System
Debian Linux

# Shell
Shell is **zsh**, not bash. Differences that bite:
- zsh expands `*` `?` `[]` `{}` `~` before the command runs, and unmatched globs error out instead of passing through.
- Quote glob chars when they are meant for the command, not the shell:
  - `rg foo -g '*.md'`
  - `find . -name '*.py'`
  - `grep --include='*.md'`
- Prefer `rg` over `grep -r` for content search.

# Zen 
The Unix philosophy, originated by Ken Thompson, is a set of cultural norms and philosophical approaches to minimalist, modular software development.
We love Unix philosophy.
YAGNI
KISS
Gall

# Output Style
Terminal UI: short, concise, no emojis. Lead with the outcome.
Objective over agreeable: no praise, no filler; disagree when facts warrant.

# File Policy
Never create docs, READMEs, markdown summaries, tests, or example files unless explicitly asked.
Prefer editing existing files over creating new ones.

# Code Style
Comments rare and one line, never a rationale.
Python: imports sorted stdlib / third-party / local; no docstrings, no `__all__`, no usage examples.

## Configuration

- Global config: `~/.config/opencode/opencode.json`

## Skills (gski)

Pip-installable package at `~/Documents/gski`. Bundles CLI tools and OpenCode SKILL.md files.
agents can use websearch skill to look info up in web

## Dotfiles Repo
Location: `~/Documents/dotfiles`
### Active Configs (`.configs/`)
All configs a simlinked to ~.configs
- hypr: hyprland.conf, hyprpaper.conf, pyprland.toml
- zsh: (.zshrc, .sh_aliases, .fzf.zsh)
- vim
- git
- lf
- keyd
- opencode
