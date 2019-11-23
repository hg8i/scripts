#!/usr/bin/env python2

"""
# Script for viewing the inards of hdf5's
"""

import h5py, sys, glob
import cPickle as pickle
from collections import defaultdict


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

def printDict(cutflow):
    for cat in cutflow.keys():
        print "-"*50
        print green(cat)
        steps = sorted(cutflow[cat].keys(), key=lambda k: -cutflow[cat][k])
        spacing = max([len(s) for s in steps])+2
        for step in steps:
            indent = spacing-len(step)
            print r"{0}{1} & {2} \\".format(step," "*indent,red(cutflow[cat][step]))
            # print green(step)," "*indent,red(cutflow[cat][step])
        print "-"*50

paths = sys.argv[1:]
# print "Reading", iPattern
nSkip=0
cutflow = defaultdict(lambda: defaultdict(lambda:0))
for path in paths:
    print "loading",path
    f = open(path,"r")
    try:
        thisCutflow = pickle.load(f)
    except:
        print red("Skipping",path)
        nSkip+=1
        continue
    for cat in thisCutflow.keys():
        if "weight" in cat: continue
        steps = sorted(thisCutflow[cat].keys())
        for step in steps:
            cutflow[cat][step]+=thisCutflow[cat][step]
printDict(cutflow)
if nSkip:
    print red("Warning: skipped {0} files".format(nSkip))
