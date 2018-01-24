#!/bin/bash

# i3-msg "move container to workspace 9"

percents=$(acpi | cut -d "," -f2 | cut -d "%" -f1)
percentsList=$(acpi | tr -d " " | tr -d "\%" | tr ":" "," | cut -d "," -f2,3 | tr "\n" ",")
currentTimeS=$(/usr/bin/date "+%s")
totalPercent=0

# Save to end of log file in /home/prime/resources/batteryPlot
echo "${currentTimeS},${percentsList}" >> /home/prime/resources/batteryPlot.txt

# sum battery percents
while read -r line; do
  let totalPercent+=$line
done <<< "$percents"

if [ $totalPercent -lt 10 ]; then
  echo "Low battery"
  i3-nagbar -m "Low battery" -b "Show battery info" "/home/prime/scripts/batteryPlot.py"
else
  echo "Good battery"
  # i3-nagbar -m "High battery" -b "Show battery info" "/home/prime/scripts/batteryPlot.py"
fi


