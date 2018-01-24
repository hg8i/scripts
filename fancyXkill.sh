#!/bin/bash
#
# kill script for the micmute/led button
# first tries kill -15, then escalates to xkill
# only one instance runs at a time, run again to cancel
# mic lights up when active, flashes for xkill
#
# to install, a couple of things are needed:
# 1) control led: /proc/acpi/ibm/led
# 2) map to button in .i3
#
# Aaron White, 2017

isRunningXprop=$(ps aux | grep xprop | grep -v grep)
isRunningXKill=$(ps aux | grep xkill | grep -v grep)

if [ -z "$isRunningXprop" ]&&[ -z "$isRunningXKill"];  then
  #"xprop not running, start it"
  /home/prime/scripts/leds.sh on mic
  #try killing nicely
  xpropResult=$(xprop)
  pid=$(echo "$xpropResult" | awk '/PID/ {print $3}')
  if [ $pid ]; then 
    kill -15 $pid
  else
    if [ "$xpropResult" ]; then #probably killed 
      /home/prime/scripts/leds.sh blink mic
      xkill
    fi
  fi
  /home/prime/scripts/leds.sh off mic
else
  #"xprop running, kill it"
  pid=$(echo $isRunningXprop | awk '{print $2}')
  if [ $pid ]; then 
    kill -15 $pid
  fi
  #"xkill running, kill it"
  pid=$(echo $isRunningXKill | awk '{print $2}')
  if [ $pid ]; then 
    kill -15 $pid
  fi
  /home/prime/scripts/leds.sh off mic
fi

