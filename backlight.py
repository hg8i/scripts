#! /usr/bin/python2
import os, sys

########################################
# configure behavior
nSteps=10 # number of luminosity steps
########################################

if len(sys.argv)>1:
  arg = sys.argv[1]
else: arg="0"

basePath="/sys/class/backlight/intel_backlight"
maxPath=os.path.join(basePath,"max_brightness")
currentPath=os.path.join(basePath,"brightness")

if arg=="up":
  mode=1
else:
  mode=0
  
#get current brightness
maxBrightness=int(open(maxPath,"r").read())

#get current brightness
currentBrightness=int(open(currentPath,"r").read())

#make list of brightnesses
stepSize=maxBrightness/nSteps
stepsList=range(stepSize,maxBrightness,stepSize)
stepsList[-1]=maxBrightness#hishest
stepsList=[0,1,20,40,100,150]+stepsList#custom points for dim

#find closest brightness to current
pos=0
while pos<len(stepsList)-1 and stepsList[pos]<currentBrightness:
  pos+=1
currentBrightness=stepsList[pos]

#pick new position for brightness
if mode==1: pos+=1
if mode==0: pos-=1
if pos<0: pos=0
if pos>len(stepsList)-1: pos=len(stepsList)-1
newBrightness=stepsList[pos]
print "position, brightness",pos, newBrightness

#write to file
print "echo {0} > {1}".format(newBrightness,currentPath)
os.popen("echo {0} > {1}".format(newBrightness,currentPath))
