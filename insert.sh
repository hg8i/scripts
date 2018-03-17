#!/bin/bash

# script to inject an insert keystroke
# context: sometimes (due to mouse shift+insert map) the keyboard gets stuck in insert state. There may be no insert button on an external keyboard, so this provides a wwork around for this problem
# 2018 Aaron White, on a plane
# Write good code.

# requires xdotool

xdotool key --clearmodifiers Insert
