#!/bin/bash
#script for modifying leds!
#requires permissions for led to be set

ledName=${2}
mode=${1}
ledPath="/proc/acpi/ibm/led"

###################
#control capslock
###################
if [ ${ledName} == "caps" ] 
  then
  if [ $mode == "on" ] 
  then
    mode=1
  else
    mode=0
  fi
  echo $mode | tee /sys/class/leds/*/brightness
  exit
fi

###################
#control ACPI led's 
###################
if [ ${ledName} == "power" ] 
then
  ledNumber=0
elif [ ${ledName} == "esc" ] 
then
  ledNumber=6
elif [ ${ledName} == "mic" ] 
then
  ledNumber=14
elif [ ${ledName} == "charger-green" ] 
then
  ledNumber=2
elif [ ${ledName} == "charger-red" ] 
then
  ledNumber=1
elif [ ${ledName} == "logo" ] 
then
  ledNumber=10
else
  ledNumber=$ledName
fi

#change led
echo "${ledNumber} ${mode}" | tee ${ledPath}


