#!/bin/bash

# script for mounting USB devices automatically

export XAUTHORITY=/home/prime/.Xauthority
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"

# sleep 10

# Mode (mount or unmount)
mode=$1
# Name for mountaing in ~/
mountName=$2
# Name in /dev, ie /dev/$devName
devName=$3


# Log of mounting activity
log="/home/prime/newLog.txt"

# udisksctl info -b /dev/${devName} >> $log 2>>$log
# notify-send "running"

# echo "mode: $mode"
# echo "=================" $(date) >> $log
# echo $@ >> $log
# echo "RUN AS: $USER" >> $log
# echo $mode $mountName $devName >> $log

# # Notification, Mount
# if [ "$mode" == "mount" ]; then
#     sleep 1
#     notify-send "Mounting ${mountName} from /dev/${devName}..."
#     echo "udisksctl mount -b /dev/${devName}" >> $log 
#     echo "============ mount  *" >> $log
#     udisksctl mount -b /dev/${devName} >> $log 2>>$log
#     echo "============ status *" >> $log
#     udisksctl status /dev/${devName} >> $log 2>>$log
#     echo "============ info   *" >> $log
#     udisksctl info -b /dev/${devName} >> $log 2>>$log
#     echo "*********" >> $log
# else
#     notify-send "Un-mounting ${mountName} from /dev/${devName}..."
#     echo "udisksctl unmount -b /dev/${devName}" >> $log
#     udisksctl unmount -b /dev/${devName} >> $log 2>>$log
# fi

# echo "DONE" >> $log
# echo " " >> $log
