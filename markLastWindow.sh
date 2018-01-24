#!/usr/bin/env bash
#marks last window in focus with "_last"
#modified to allow only ONE instance
#https://www.reddit.com/r/i3wm/comments/4d4luc/how_to_focus_the_last_window/

/home/prime/scripts/flashesc

#quit if other instance is running
isRunning=$(ps aux | grep markLastWindow.sh | grep -v grep | grep -v vim | wc -l)
echo $isRunning
if [ "$isRunning" != "2" ]; then
  echo "running, so quitting"
  exit
else
  echo "not running, so continuing"
fi
last=

xprop -root -spy _NET_ACTIVE_WINDOW | while :
do
    read line

    [[ -z "$last" ]] || i3-msg "[id=$last] mark _last"
    last=$(echo "$line" | awk -F' ' '{printf $NF}')
    echo $(date)>/home/prime/a
done
