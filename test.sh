#!/bin/sh
Xephyr -ac -screen 1920x1080 -br -reset -terminate :1 &
sleep 1
DISPLAY=:1
xterm -geometry 100x50
