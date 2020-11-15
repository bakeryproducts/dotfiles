#!/bin/bash
picom & 
nitrogen --set-zoom-fill ~/Downloads/wp.jpg
xrdb ~/.Xresources
setxkbmap -option caps:escape &
xset r rate 220 50 &
clipmenud &
