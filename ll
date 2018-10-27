#!/bin/bash
# Fancy ls, only print size, date, and name
#Aaron White, 2017

result=$(/bin/ls ${@} --color=always -lrth)

# PRINTOUT LINES IN NICE PRESENTATION
if [ $(echo "$result" | wc -l) -eq 1 ]; then
  echo "$result" | awk "{print \$5 \"\\t\" \$6 \$7 \" \" \$8 \"\\t\" \$9}"
else 
  echo "$result" | tail -n +1 | awk "{print \$5 \"\\t\" \$6 \$7 \" \" \$8 \"\\t\" \$9}"
fi

# COPY FINAL LINE TO XCLIP (if it exists)
if [ $(command -v xclip) ]; then
    # get final line (most recently modified file)
    mostRecent=$(echo "$result" | tail -n 1 | awk "{print \$9}")
    # remove color formatting (match control sequences)
    mostRecent=$(echo $mostRecent | sed -r "s/[[:cntrl:]]\[[0-9]+[;0-9]*m//g")
    # copy to xclip
    echo $mostRecent | tr -d "\n" | xclip
fi

