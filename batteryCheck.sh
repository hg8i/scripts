#!/bin/bash
# keep a log of the battery state

# Start timer, as root
# systemctl start batteryCheck.timer
# Enable timer to start at boot
# systemctl enable batteryCheck.timer

# https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files

percentsList=$(acpi | tr -d " " | tr -d "\%" | tr ":" "," | cut -d "," -f2,3 | tr "\n" ",")
currentTimeS=$(/usr/bin/date "+%s")

# Save to end of log file in /home/prime/resources/batteryPlot
echo "${currentTimeS},${percentsList}" >> /home/prime/resources/batteryPlot.txt
