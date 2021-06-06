setxkbmap -option caps:escape
setxkbmap -layout us,bg -option grp:menu_toggle 
pgrep mpd || ( mpd && mpc play ) &
picom &
parcellite &
randomwall &
slstatus &
dunst &
xrdb -merge ~/.Xresources &
redshift -P -O 4500K &
transmission-daemon &
#pipewire &
#pipewire-pulse &
(sleep 1 && xterm) &
exec ./tueswm
