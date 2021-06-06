#!/bin/sh
Xephyr -ac -screen 1920x1080 -br -reset -terminate :1 &
DISPLAY=:1
(sleep 1 && xterm) &
exec ./tueswm
