# Dotfiles Repository

Personal configuration files for Linux systems.

## Structure

```
dotfiles/
├── .configs/
│   └── archive/       # Legacy configs
├── .local/
│   ├── bin/           # Custom scripts
│   │   ├── sshw       # SSH wrapper
│   │   └── termnot2   # Terminal notifications
│   ├── link-bins      # Script to symlink bins to ~/.local/bin
│   └── link-cfgs      # Script to symlink configs to ~/.config
├── setup/
│   ├── install-iosevka.sh    # Iosevka Nerd Font installer
│   └── programs/
│       ├── alacritty.sh      # Alacritty install
│       └── docker.sh         # Docker install
├── .bashrc            # Bash config (fallback)
└── .gitignore
```

## Installation

```bash
# Link configs
cd .local && ./link-cfgs

# Link custom scripts
cd .local && ./link-bins
```

## Current Status

### Active Configs
- **hypr**: Primary window manager (Hyprland)
- **zsh**: Primary shell
- **vim**: Editor
- **git**: Version control
- **lf**: File manager

### Archived (in `.configs/archive/`)
- i3, qtile, ranger, picom, urxvt, xs - legacy X11/old WM configs
