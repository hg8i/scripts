#!/bin/bash

#launch web
singleWorkspace -n :web
chromium --new-window "http://email.umich.edu/"\
                      "https://twiki.cern.ch/twiki/bin/view/Atlas/WebHome" &
sleep 1
#launch UMT tabs
singleWorkspace -n :ana
launchumt.sh
sleep 0.3
#launch stack
singleWorkspace -n :stk
urxvt -e bash -c "cd /home/prime/stack; vim hmumu.txt; bash" &
#launch slides
sleep 0.3
singleWorkspace -n :sld
urxvt -e bash -c "cd /home/prime/latex; bash" &

#move workspaces to input h (for hmumu)
workspace l h
