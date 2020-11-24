#!/bin/bash
picom & 
nitrogen --set-zoom-fill ~/Downloads/wp.jpg
xrdb ~/.config/xs/.Xresources
setxkbmap -option caps:escape &
xset r rate 220 50 &
clipmenud &
