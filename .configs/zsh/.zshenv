# Don't error on unmatched globs; pass the pattern through like bash
unsetopt nomatch

. "$HOME/.cargo/env"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
export PATH="$HOME/miniconda3/bin:$PATH"
