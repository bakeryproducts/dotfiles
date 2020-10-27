
alias rr='ranger'
alias cc='clean'
alias ls='ls --color=auto'
alias ll='ls -alFh'
alias la='ls -A'
alias l='ls -CF'
#alias si='ssh $DB7USER@$DB7HOST'
#alias sj='echo $DB7USER'

zz()
{
cd `fasd_cd -d -R | fzf | awk '{print $2}'`
}
