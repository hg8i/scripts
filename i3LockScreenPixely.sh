#!/bin/bash

scrot /tmp/screen_locked.png

convert -scale 10% -scale 1000% /tmp/screen_locked.png /tmp/screen_locked.png

# i3lock -p win -i /home/prime/.i3/macScreenshotForLock.png
i3lock -p win -i /tmp/screen_locked.png
