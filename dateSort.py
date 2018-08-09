#!/usr/bin/env python2

# script for sorting files by dates
# searches filenames for 6 digit date
# sets access time with touch

import glob, sys, os, re

def extractDataFromFilename(f):
    # extract 6 digit date string from filename, return as touch-compatable date
    # if not exist, return unix epoch
    p = re.compile('\d+')
    allNumbers = p.findall(f)
    sixDigitNum= [ d for d in allNumbers if len(d)==6]
    if len(sixDigitNum)==0: return "197001010000"
    if len(sixDigitNum)!=1:
        print "Picking date",sixDigitNum[0], "of possible dates", sixDigitNum
    num = sixDigitNum[0]
    day= num[0:2]
    month= num[2:4]
    year= num[4:6]
    return "20"+year+month+day+"0000"



# get input directory
if len(sys.argv)>1:
    path = sys.argv[1]
else:
    path = "./"

# get files
files=glob.glob("{0}/*".format(path))
# get just file names
files = [os.path.basename(f) for f in files]

cmd="touch -t {0} {1}"

for f in files:
    date = extractDataFromFilename(f)
    thisCmd = cmd.format(date,f)
    # print thisCmd
    os.popen(thisCmd)
