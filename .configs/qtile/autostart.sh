#!/bin/bash
#picom -f & 
#nitrogen --set-zoom-fill ~/Downloads/wp.jpg
xrdb ~/.config/xs/.Xresources
setxkbmap -option caps:escape 
xset r rate 220 50 &
clipmenud &
xmodmap -e 'remove mod1 = Alt_R' 
xmodmap -e 'add control = Alt_R' 
