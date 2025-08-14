export ZSH="/home/$USER/.oh-my-zsh"
ZSH_THEME="nicoulaj"
DISABLE_AUTO_UPDATE="true"
DISABLE_UPDATE_PROMPT="true"
#ENABLE_CORRECTION="true"
plugins=(git extract)
HISTFILE=~/.config/zsh/.zsh_history
source $ZSH/oh-my-zsh.sh
KEYTIMEOUT=8


# History
HISTSIZE=100000000
SAVEHIST=100000000
setopt HIST_IGNORE_SPACE
setopt extended_history
setopt hist_expire_dups_first
setopt hist_ignore_dups # ignore duplication command history list
setopt hist_ignore_space
setopt hist_verify
setopt inc_append_history
setopt share_history # share command history data

# Vi

bindkey -v

# Use vim keys in tab complete menu:
bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'l' vi-forward-char
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -v '^?' backward-delete-char

autoload edit-command-line; zle -N edit-command-line
bindkey '^e' edit-command-line


function zle-keymap-select {
  if [[ ${KEYMAP} == vicmd ]] ||
     [[ $1 = 'block' ]]; then
    echo -ne '\e[1 q\033]12;Green\007'
  elif [[ ${KEYMAP} == main ]] ||
       [[ ${KEYMAP} == viins ]] ||
       [[ ${KEYMAP} = '' ]] ||
       [[ $1 = 'beam' ]]; then
    echo -ne '\e[5 q\033]12;Grey\007'
  fi
}
zle -N zle-keymap-select

zle-line-init() {
    zle -K viins 
    echo -ne "\e[5 q"
}
zle -N zle-line-init

_fix_cursor() {
   echo -ne '\e[5 q'
}

precmd_functions+=(_fix_cursor)
zle-line-finish() { echo -ne "\e[2 q" }

# prepend sudo
sudo-command-line() {
    [[ -z $BUFFER ]] && zle up-history
    [[ $BUFFER != sudo\ * ]] && BUFFER="sudo ${BUFFER% }"
    zle end-of-line
}
zle -N sudo-command-line
bindkey "\es" sudo-command-line



# User configuration
bindkey "^k" history-search-backward
bindkey "^j" history-search-forward

# export LANG=en_US.UTF-8
# export LC_ALL="en_US.UTF-8"
export EDITOR='vim'

alias zshcfg="vim ~/.zshrc"
alias vimcfg="vim ~/.config/vim/vimrc"
# alias astcfg="vim ~/.config/qtile/autostart.sh"
# alias qticfg="vim ~/.config/qtile/config.py"
alias wmcfg="vim ~/.config/hypr/hyprland.conf"
alias ohmyzsh="vim ~/.oh-my-zsh"

export MYVIMRC="~/.config/vim/vimrc"
export VIMINIT=":set runtimepath+=~/.config/vim|:source $MYVIMRC"
export KAGGLE_CONFIG_DIR=~/.config/kaggle/


if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/.cargo/bin" ] ; then
    PATH="$HOME/.cargo/bin:$PATH"
fi

if [ -d "$HOME/miniconda3/bin" ] ; then
    PATH="$HOME/miniconda3/bin:$PATH"
fi

if [ -f ~/.sh_aliases ]; then
    . ~/.sh_aliases
fi


eval "$(fasd --init posix-alias zsh-hook)"
[ -f ~/.config/zsh/.fzf.zsh ] && source ~/.config/zsh/.fzf.zsh 


if uwsm check may-start; then
    exec uwsm start hyprland-uwsm.desktop
fi
