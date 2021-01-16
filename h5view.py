#!/usr/bin/env python2
from collections import defaultdict

"""
# Script for viewing the inards of hdf5's
"""

import h5py, sys, glob

def red(*string):
    """ return string as red """
    string = [str(s) for s in string]
    ret = "\033[31m{0}\033[39m".format(" ".join(string))
    return ret

def green(*string):
    """ return string as green """
    string = [str(s) for s in string]
    ret = "\033[32m{0}\033[39m".format(" ".join(string))
    return ret

if "-w" in sys.argv:
    sumName = sys.argv[2]
    paths = sys.argv[3:]
else: 
    sumName = None
    paths = sys.argv[1:]

# print "Reading", iPattern


# paths = glob.glob(iPattern)
# print "Reading",paths
numberOfEventsAll = 0
numberOfEventsByCat = defaultdict(int)
for path in paths:
    print "Showing",path
    iFile = h5py.File(path,"r")
    for k in iFile.attrs.keys(): print k,":\t",iFile.attrs[k]
    print "\tCat \t#Vars\t#{}".format(sumName if sumName else "Entries")
    numberOfEvents = 0
    for cat in iFile.keys():
        varLengths = set([len(iFile[cat][v]) for v in iFile[cat].keys()])
        nEvents=0
        if len(varLengths)>1:
            lenString = red("Length miss-match: {0}".format(varLengths))
        elif len(varLengths)==1:
            nEvents = varLengths.pop()
            numberOfEvents+=nEvents
            lenString = green(nEvents)
        else:
            lenString = "None"
        # if summing up weights, replace lenString with sum
        if sumName!=None:
            lenString=sum(iFile[cat][sumName])
            nEvents=float(lenString)
        print "\t{0}\t{1}\t{2}".format(cat,len(iFile[cat]),lenString)
        numberOfEventsByCat[cat]+=nEvents
        # print iFile[cat].keys()
    print "\tTotal: {0}".format(numberOfEvents)
    numberOfEventsAll+=numberOfEvents

print "="*50
print green("Total in all files: {0}".format(numberOfEventsAll))
for cat in numberOfEventsByCat.keys():
    print green(cat, numberOfEventsByCat[cat])



