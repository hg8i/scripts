#! /usr/bin/python2
import os, sys
#os.popen("/home/prime/scripts/flashesc")


def markWindow():
  #get window data 
  rawdata=os.popen('xprop -root _NET_ACTIVE_WINDOW').read()
  #convert data to python
  windowid=rawdata.split()[-1]

  #mark window
  os.popen('i3-msg "[id={0}] mark _last"'.format(windowid))

def jumpWindow():
  os.popen('i3-msg "[con_mark=_last] focus"')


arg=sys.argv[1]
if arg=="mark":
  markWindow()
elif arg=="jump":
  jumpWindow()
else:
  pass

