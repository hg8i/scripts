#!/usr/bin/env python2

# python script to change volume, update user with current volume
# arguement is either up or down, ie:
# python volume.py up

import sys, os

# arguement
if len(sys.argv)<2:
  print "#"*50
  print "Please give proper arguement"
  print "\tUsage:"
  print "\tvolume.py [arg]"
  print "\targ is either 'up' or 'down' or 'mute'"
  print "#"*50
  quit()
arg = sys.argv[1]

print "Running with arguement:", arg

# change volume
if arg=="up":
  os.popen("pactl set-sink-volume 0 +5%")
elif arg=="down":
  os.popen("pactl set-sink-volume 0 -5%")
elif arg=="mute":
  os.popen("pactl set-sink-mute 0 toggle")
else:
  print "Bad arguement"
  quit()

# make notification
def makeVolume():
  import re
  amixer=os.popen("amixer sget Master").read()
  percents=re.compile("\d\d%").findall(amixer)
  # volume=" ".join(percents)
  volume=percents[0]
  return volume

def makeMute():
  # return mute state
  amixer=os.popen("amixer sget Master").read()
  if "[off]" in amixer: return "mute"
  return "un-mute"




muteString=""
if arg=="mute": 
  msg="State: {0}".format(makeMute())
else:
  msg="Volume: {0}".format(makeVolume())
notifyString="notify-send --expire-time 500 --urgency=normal '{0}'"
notifyString=notifyString.format(msg)
os.popen(notifyString)
