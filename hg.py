#!/usr/bin/env python2
##! /usr/bin/python2.6
from __future__ import division
import os, sys, re
import subprocess 
from math import log
from os.path import expanduser

def histToList():
  #histPath="/afs/atlas.umich.edu/home/aaronsw/.bash_history"
  histPath=expanduser("~/.bash_history")
  hist=open(histPath,"r").readlines()
  return hist

def searchHist(hist, pattern):
  filteredHist=[]
  red="\033[1m\033[31m{0}\033[0m\033[39m\033[49m"
  for oline in reversed(hist):
    if pattern in oline and oline[:3] != "hg ":
      line=re.sub(pattern,red.format(pattern),oline,re.IGNORECASE)
      newentry=[line[:-1],oline]
      if newentry not in filteredHist:
	filteredHist.append(newentry)
  filteredHist.reverse()
  return filteredHist

def wrapText(pattern,indentSize, availSize, text):
  green="\033[1m\033[32m{0}\033[0m\033[39m\033[49m"
  red="\033[1m\033[31m{0}\033[0m\033[39m\033[49m"
  bold="\033[1m{0}\033[0m"
  wrappedString=""
  while not text.isspace():
    wrappedString+=text[0:availSize]+"\n"
    text=" "*indentSize+text[availSize:]
  #remove whitespace from end of string
  wrappedString=re.sub("\s*$","",wrappedString)
  #color search pattern
  if pattern!="":
    wrappedString=re.sub(pattern,red.format(pattern),wrappedString)
  #color pipes after numbers
  wrappedString=re.sub('([0-9]*\s*)\|',r'\1'+green.format("|") ,wrappedString)
  #add pipes on new lines
  wrappedString=re.sub("\n\s{{{0}}}".format(indentSize),\
                       green.format(" "*(indentSize-2)+"| "),\
		       wrappedString)
  #bold numbers
  wrappedString=re.sub('^([0-9]+)',bold.format(r'\1'),wrappedString)
  return wrappedString

def realLen(s):
  reals=re.sub("\033\[[0-9]*m","",s)
  return len(reals)

def printHist(hist,pattern):
  green="\033[1m\033[32m{0}\033[0m\033[39m\033[49m"
  bold="\033[1m{0}\033[0m"
  maxNumLen=int(log(max(1,len(hist)),10)+2)
  for i, lineBoth in enumerate(hist):
    num=str(len(hist)-i)
    numberPart=num+" "*(maxNumLen-len(num))+"| "
    commandPart=lineBoth[1]
    print wrapText(pattern,realLen(numberPart),columns,numberPart+commandPart)

def exCommandByNumber(hist,writeCommandPath):
  n=raw_input("Enter number: ")
  if n=="q": quit()
  try: n=int(n)
  except:
    print "quitting..."
    quit()
  if n>len(hist):
    print "Bad number"
    return False
  else:
    command=hist[len(hist)-n][1]
    print "Good number, running", command
    print "#"*20
    #save command to pipe file
    f=open(writeCommandPath,"w")
    f.write(command)
    ##execute command through subprocess
    #sp = subprocess.Popen(["/bin/bash", "-i", "-c", command])
    #sp.communicate()
    return True

def run(pattern,writeCommandPath):
  hist=histToList()
  #trim hist
  del hist[-1]
  filteredHist=searchHist(hist, pattern)
  filteredHist=filteredHist[-maxSearch:]
  printHist(filteredHist,pattern)
  while not exCommandByNumber(filteredHist,writeCommandPath):
    pass

if len(sys.argv)<3:
  searchFor=""
  maxSearch=90
  writeCommandPath=""
else:
  writeCommandPath=sys.argv[1]
  searchFor=" ".join(sys.argv[2:])
  maxSearch=30

rows, columns = os.popen('stty size', 'r').read().split()
columns=int(columns)

run(searchFor, writeCommandPath)
#print wrapText(8,30,"#"*300)


