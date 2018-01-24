#!/bin/bash
#resize all images in directory
#first arguement must be a size, in pixels

size=$1
c=0
for fileName in $@
do 
    let c+=1
    if [ $c -lt 2 ]; then continue; fi
    echo resizing $fileName $c to size ${size}....
    direct=$(dirname "$fileName")
    filename=$(basename "$fileName")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo "$fileName" -resize ${size}x${size} "${direct}/${size}x${size}-${filename}.${extension}" ; 
    convert "$fileName" -resize ${size}x${size} "${direct}/${size}x${size}-${filename}.${extension}" ; 
done

