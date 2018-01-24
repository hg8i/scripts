#!/bin/bash

#kill workspace by name, $1
workspaceName=$1

#move to desired workspace
i3-msg "workspace ${1}"
#select all windows in workspace
repeat 10 i3-msg focus parent
#kill selected windows
#jump back to original workspace
# i3-msg "workspace back_and_forth"
