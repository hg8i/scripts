#! /usr/bin/python2
import os, sys

if len(sys.argv)>1:
  arg = sys.argv[1]
else: arg="0"

basePath="/sys/class/leds/tpacpi::kbd_backlight"
maxPath=os.path.join(basePath,"max_brightness")
currentPath=os.path.join(basePath,"brightness")

if arg=="up":
  mode=1
else:
  mode=0
  
#get current brightness
maxBrightness=2

#get current brightness
currentBrightness=int(open(currentPath,"r").read())

#make list of brightnesses
stepsList=[0,1,2]

#find closest brightness to current
pos=0
while pos<len(stepsList)-1 and stepsList[pos]<currentBrightness:
  pos+=1
pos+=1

if pos>len(stepsList)-1: pos=0
newBrightness=stepsList[pos]
print "position, brightness",pos, newBrightness

#write to file
os.popen("echo {0} > {1}".format(newBrightness,currentPath))
