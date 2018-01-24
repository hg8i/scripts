#!/bin/bash
# warning if battery drops below some threshold
# I tried to run this a systemd timer, but had touble getting the notification to pass to the display
# Instead, this should be run by .i3/conf:
	# watch -n 300 /home/prime/scripts/batteryWatch.sh

percents=$(acpi | cut -d "," -f2 | cut -d "%" -f1)
totalPercent=0

# sum battery percents
while read -r line; do
  let totalPercent+=$line
done <<< "$percents"
echo "totalPercent:${totalPercent}"

danger=10
warning=20
if [ $totalPercent -gt $danger -a $totalPercent -lt $warning ]; then
  echo "Low battery"
  notify-send "Low battery" --expire-time 2 --urgency=normal "$totalPercent"
elif [ $totalPercent -lt $danger ]; then
  echo "No battery"
  notify-send "No battery!" --urgency=critical "$totalPercent"
else
  echo "Good battery"
fi


