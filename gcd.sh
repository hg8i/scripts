#!/bin/bash

#global save or goto directory
#should be run with an alias to run in shame shell

echo "Arguements: save, go (default). Add source alias to bashrc."
mode=$1

if [ -z $1 ]; then
  echo "assuming default arguement go"
  mode="go"
fi

if [ $mode == "save" ]; then
  echo "saving directory"
  echo $(pwd) is saved
  echo $(pwd) > ~/.tmpSavedDir
elif [ $mode == "go" ]; then
  echo "going to directory"
  echo $(cat ~/.tmpSavedDir)
  cd $(cat ~/.tmpSavedDir)
else
  echo "give an arguement:"
  echo "use mode save or go"
fi

