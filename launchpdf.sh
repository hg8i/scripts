#!/bin/bash

i3-msg "append_layout ~/.i3/workspace-PDF.json"

sleep 0.2

#launch vifm
urxvt -name "vifm-term" -xrm "*background: #000000" -e bash -c "vifm +runForPdf ~/pdfs/otherSlides ~/pdfs/mySlides; bash" &
#launch evince
evince 2>/dev/null &
