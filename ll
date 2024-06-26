#!/bin/bash
# Fancy ls, only print size, date, and name
#Aaron White, 2017
#Updated Jan 2024 to handle spaces in file names

result=$(/bin/ls ${@} --color=always -lrth)
first_word="${result%% *}"

# echo ${@}
# echo ${#}
# echo "--------------------------------------------------"
# /bin/ls ${@} --color=always -lrthq
# echo "--------------------------------------------------"
# echo "First:" $first_word
# echo "--------------------------------------------------"


# if [ ${#} -lt 2 ]; then
if [ "$first_word" == "" -o  "$first_word" == "total" ]; then
    echo "$result" | tail -n +2 | awk '{printf "%s\t%s %s\t%s ",$5,$6,$7,$8; for(i=9; i<NF+1; i++) printf "%s%s",$i,(i<NF ? "\\ " : RS)}'
else 
    # echo $result
    # echo "$result" | head -n +1
    # tail cuts off the "total" line
    echo "$result" | awk '{printf "%s\t%s %s\t%s ",$5,$6,$7,$8; for(i=9; i<NF+1; i++) printf "%s%s",$i,(i<NF ? "\\ " : RS)}'
fi


# COPY FINAL LINE TO XCLIP (if it exists)
if [ $(command -v xclip) ] && [ $DISPLAY ]; then
    # get final line (most recently modified file)
    mostRecent=$(echo "$result" | tail -n 1 | awk '{for(i=9; i<NF+1; i++) printf "%s%s",$i,(i<NF ? "\\ " : RS)}')
    # remove color formatting (match control sequences)
    mostRecent=$(echo $mostRecent | sed -r "s/[[:cntrl:]]\[[0-9]+[;0-9]*m//g")
    # copy to xclip
    echo $mostRecent | tr -d "\n" | xclip
fi

