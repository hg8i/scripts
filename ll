#!/bin/bash
#fancy ls, only print size, date, and name
#Aaron White, 2017

result=$(/bin/ls ${1} --color=always -lrth)

if [ $(echo "$result" | wc -l) -eq 1 ]; then
  echo "$result" | awk "{print \$5 \"\\t\" \$6 \$7 \" \" \$8 \"\\t\" \$9}"
else 
  echo "$result" | tail -n +2 | awk "{print \$5 \"\\t\" \$6 \$7 \" \" \$8 \"\\t\" \$9}"
fi

