
export ZSH="/home/gsm/.oh-my-zsh"
ZSH_THEME="agnoster"
DISABLE_AUTO_UPDATE="true"
DISABLE_UPDATE_PROMPT="true"
ENABLE_CORRECTION="true"
plugins=(git)
HISTFILE=~/.config/zsh/.zsh_history
source $ZSH/oh-my-zsh.sh

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




# User configuration

export LANG=en_US.UTF-8

export EDITOR='vim'

alias zshcfg="vim ~/.config/zsh/.zshrc"
alias ohmyzsh="vim ~/.oh-my-zsh"

export MYVIMRC="~/.config/vim/vimrc"
export VIMINIT=":set runtimepath+=~/.config/vim|:source $MYVIMRC"


if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

if [ -f ~/.sec_glebash ]; then
    . ~/.sec_glebash
    git config --global user.name "$GITUSER"
    git config --global user.email "$GITMAIL"
fi

if [ -f ~/.glebash ]; then
    . ~/.glebash
fi

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

#eval "$(fasd --init auto)"
[ -f ~/.config/zsh/.fzf.zsh ] && source ~/.config/zsh/.fzf.zsh 
