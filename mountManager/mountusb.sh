#!/bin/bash

# script for mounting USB devices automatically

export XAUTHORITY=/home/prime/.Xauthority
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"
export USER="prime"

log="/home/prime/mountlog.txt"
echo "==============" >> $log
echo $1 >> $log
echo $2 >> $log
echo $3 >> $log

mode=$1
block="/dev/$2"

# look up filesystem name
name=$(e2label ${block})
if [ -z "$name" ]; then
    name="default"
fi
linkPath="/home/prime/${name}"
mountPath="/run/media/system/${name}"

echo "Mounting block:"
echo $block
echo "Mounting name:"
echo $name
echo "Link path:"
echo $linkPath
echo "Mount path:"
echo $mountPath

rm /home/prime/debug

if [ "$mode" == "mount" ]; then
    sudo -u $USER DISPLAY=$DISPLAY DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS notify-send "Mounting ${name} from /dev/${2}..."
    # mount command
    echo "===> Running mount command:"
    # echo $(systemd-mount ${block})
    # echo $(systemd-mount --collect ${block} $mountPath)
    # echo $(sudo udisksctl mount -b ${block} ${mountPath})
    echo $(sudo -u $USER udisksctl mount -b ${block}) >> /home/prime/debug 2>>/home/prime/debug
    # chown prime:prime $mountPath
    # link to home directory
    # echo UNLINK: $(unlink $linkPath)
    echo LINK:   $(ln -s $mountPath $linkPath)
elif [ "$mode" == "unmount" ]; then
    sudo -u $USER DISPLAY=$DISPLAY DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS notify-send "Unmounting ${name} from /dev/${2}..."
    echo UNLINK:  $(unlink $linkPath)
    echo "===> Running unmount command:"
    sudo udisksctl unmount -b ${block} >> /home/prime/debug 2>>/home/prime/debug
    # echo UNMOUNT: $mountPath $(systemd-umount $mountPath)
else
    sudo -u $USER DISPLAY=$DISPLAY DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS notify-send "Invalid mount mode"
    echo "Invalid mode"
fi

sudo -u $USER DISPLAY=$DISPLAY DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS notify-send "DONE"
