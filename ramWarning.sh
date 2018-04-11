#!/bin/bash
# warning if available RAM drops below some threshold
# I tried to run this a systemd timer, but had touble getting the notification to pass to the display
# Instead, this should be run by .i3/conf:
	# watch -n 300 /home/prime/scripts/batteryWatch.sh


totalFreeMem=$(free -m | sed -n '/Mem/s/ \+/ /gp' | cut -d ' ' -f7)

danger=1000
warning=2000
if [ $totalFreeMem -gt $danger -a $totalFreeMem -lt $warning ]; then
	echo "Low RAM"
	notify-send "Low RAM" --expire-time 2 --urgency=critical "Total Memory Remaining: $totalFreeMem MB"
elif [ $totalFreeMem -lt $danger ]; then
	echo "Critical RAM"
	notify-send "### Critical RAM! ###" --urgency=critical "Toatl Memory Remaining: $totalFreeMem MB"
else
	echo "Good Ram"
fi

