# Setup fzf
# ---------
if [[ ! "$PATH" == */home/gsm/.fzf/bin* ]]; then
  export PATH="${PATH:+${PATH}:}/home/gsm/.fzf/bin"
fi

# Auto-completion
# ---------------
[[ $- == *i* ]] && source "/home/gsm/.fzf/shell/completion.zsh" 2> /dev/null

# Key bindings
# ------------
source "/home/gsm/.fzf/shell/key-bindings.zsh"
