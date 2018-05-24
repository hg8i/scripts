#!/usr/bin/env python2

# script for toggeling certain laptop settings (xmodmap, xrandr), depending on situation
# This script:
#   * Increments the state
#   * Sends the user a notificaiton with the new state
#
# State scripts are stored in ./states in a convienant format

# current state is stored as a file name in ./currentState.txt
import sys,os, re

def executeState(statePath):
  # run the commands in provided state file
  commands = open(statePath,"r").readlines()
  # remove whitespace at start of line
  commands = [ x.replace("\n","") for x in commands ]
  commands = [ x.strip() for x in commands if x!=""]
  # ignore comments
  commands = [ x for x in commands if x[0] not in ["#","\n"] ]
  # break up commands by label, arguements
  commands = [ (x[:x.find(":")],x[x.find(":")+1:]) for x in commands ]

  # execute commands
  for instruction in commands:
    com = instruction[0].strip()
    arg = instruction[1]
    exe = "echo default"
    if com == "name":
      exe = 'notify-send "Switched to use state: {0}" --expire-time 2000 --urgency=normal'.format(arg)
    elif com == "run":
      exe = os.popen(arg).read()
    elif com == "xrandr":
      exe = "xrandr {0}".format(arg)
    elif com == "xmodmap":
      exe = "xmodmap {0}".format(arg)

    print "="*50
    print instruction
    print repr(exe)
    result = os.popen(exe).read()
    # print repr(result)



installPath = sys.path[0]
curStatePath = os.path.join(installPath, "currentState.txt")
curState = open(curStatePath,"r").read().strip()

print "Current state is stored in:", curStatePath
print "Running on ", curState

# get list of states in the state dir
statesPath = os.path.join(installPath, "states")
states = os.listdir(statesPath)
states = filter(lambda p: p[0]!=".", states)
if len(states) == 0:
  raise BaseException("There are no states found in directory: {0}".format(statesPath))
print "states", states

# get index of curState in states
# there must be at least one state
if curState in states:
  index = states.index(curState)
else:
  index = 0

# increment to next state
index = (index+1) % len(states)
print "New state", states[index]
curState = states[index]

# save current state into currentState.txt
curStateFile = open(curStatePath,"w")
curStateFile.write(curState)

# execute the parameters of curstate
curState= os.path.join(statesPath,curState)
executeState(curState)

print "Finished"
