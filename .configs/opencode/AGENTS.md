# Global Agent Instructions

# System
Debian Linux

# Zen 
The Unix philosophy, originated by Ken Thompson, is a set of cultural norms and philosophical approaches to minimalist, modular software development.
We love Unix philosophy.
YAGNI
KISS
Gall

## Configuration

- Global config: `~/.config/opencode/opencode.json`

## MCP Servers

- **vault**: Personal vault/notes access
- **context7**: Up-to-date library documentation

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


## Tickets
When working on a project

Local file-based ticket system. Only use when explicitly requested.

```
tickets/
├── GUIDE.md           # ticket writing guide
├── registry.json      # index with id, title, priority, status, created
├── G-002-feature.md   # active tickets
└── done/
    └── G-001-feature.md   # completed/cancelled tickets
```

**States:** `open`, `in_progress`, `done`, `cancelled`
**Priorities:** `high`, `medium`, `low`

### Workflow

**Create ticket:**
1. Add entry with status `open`
2. Create `tickets/G-XXX-slug.md`

**Complete ticket:**
1. Update status to `done` in registry
2. Move file: `mv tickets/G-XXX-slug.md tickets/done/`
3. Append fix summary to the moved file:
   - Files changed (paths)
   - What was done (1-2 lines)
   - Any notable decisions
