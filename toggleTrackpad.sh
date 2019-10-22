#!/bin/bash

# script to toggle xinput of trackpad based on name
# is more reliable than hardcoding the id
# takes arguement for on/off: 0, 1

echo "Usage: arguement=0 or arguement=1"
if [ "$#" -lt 1 ]; then 
    onoff=0
else
    onoff=$1
fi

# find trackpad info line
line=$(xinput -list | grep TouchPad)
# find trackpad id
id=-1
for word in $line; do
	if [[ $word == *"id="* ]]; then
		id=$(echo $word | cut -d "=" -f2)
		echo "found id=$id"
		break
	fi
done

# change the state
xinput set-prop $id "Device Enabled" $onoff
