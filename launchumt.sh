#!/bin/bash

i3-msg "append_layout /home/prime/.i3/workspace-2:ANA.json"

sleep 0.2
atlasGreen=e0f0e0
atlasBlue=e0e0f0
white=ffffff
cmd="umt"

urxvt -name "umtl1" -xrm "*background: #${white}" -e bash -c "sleep 55; ${cmd} ; bash" &
urxvt -name "umtl2" -xrm "*background: #${white}" -e bash -c "sleep 45; ${cmd} ; bash" &
urxvt -name "umtl3" -xrm "*background: #${white}" -e bash -c "sleep 35; ${cmd} ; bash" &
urxvt -name "umtl4" -xrm "*background: #${white}" -e bash -c "sleep 25; ${cmd} ; bash" &
urxvt -name "umtl5" -xrm "*background: #${white}" -e bash -c "sleep 15; ${cmd} ; bash" &
urxvt -name "umtl6" -xrm "*background: #${white}" -e bash -c "sleep 05; ${cmd} ; bash" &

urxvt -name "umtr1" -xrm "*background: #${atlasGreen}" -e bash -c "sleep 00; ${cmd} ; bash" &
urxvt -name "umtr2" -xrm "*background: #${atlasGreen}" -e bash -c "sleep 10; ${cmd} ; bash" &
urxvt -name "umtr3" -xrm "*background: #${atlasGreen}" -e bash -c "sleep 20; ${cmd} ; bash" &
urxvt -name "umtr4" -xrm "*background: #${atlasGreen}" -e bash -c "sleep 30; ${cmd} ; bash" &

sleep 0.1
i3-msg "[instance=umtl6] focus"
sleep 0.1
i3-msg "[instance=umtr1] focus"
