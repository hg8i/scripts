#!/bin/bash

# script for mounting USB devices automatically

export XAUTHORITY=/home/prime/.Xauthority
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"


# Mode (mount or unmount)
mode=$1
# Name for mountaing in ~/
mountName=$2
# Name in /dev, ie /dev/$devName
devName=$3

# Log of mounting activity
log="/home/prime/mountLog.txt"
echo $mode $mountName $devName $(date) >> $log

# Notification, Mount
if [ "$mode" == "mount" ]; then
    notify-send "Mounting ${mountName} from /dev/${devName}..."
    udisksctl mount -b /dev/${devName}
else
    notify-send "Un-mounting ${mountName} from /dev/${devName}..."
    udisksctl unmount -b /dev/${devName}
fi

