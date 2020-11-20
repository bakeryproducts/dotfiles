alias rr='ranger'
alias cc='clear'
alias ls='ls --color=auto'
alias ll='ls -alFh'
alias la='ls -A'
alias l='ls -CF'
#alias si='ssh $DB7USER@$DB7HOST'
alias sai='sudo apt install'
alias sau='sudo apt update'
alias restart='sudo shutdown -r now'

#zz()
#{
#cd `fasd_cd -R | fzf | awk '{print $2}'`
#}

si()
{
ssh -t $DB7USER@$DB7HOST env SFTPPASS=$SFTPPASS env SFTPUSER=$SFTPUSER bash
}
