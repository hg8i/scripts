#! /bin/env python2

"""
# Script to clean out files from figures/ that are not
# in slides.tex
"""

import os, re, glob

print os.getcwd()

pattern = re.compile(r"includegraphics.*figures/")
linesWithFigures = [l for l in open("slides.tex") if pattern.search(l)]
print "Lines with figures", len(linesWithFigures)

pattern = re.compile(r"(?<={)figures/.*?(?=}[^\.])")
usedFigurePaths = [pattern.search(l).group() for l in linesWithFigures]
usedFigurePaths = [re.sub("[{}]","",l) for l in usedFigurePaths]

# for i in usedFigurePaths:
#     if "m_ll_const.ee_m_eebins_log100" not in i: continue
#     print i
# quit()

nDel,nSave = 0,0
for dirpath, dirnames, filenames in os.walk("figures"):
    # print dirpath, dirnames, filenames
    print dirpath
    # print filenames
    for filename in filenames:
        # if "m_ll_const.ee_m_eebins_log100" not in filename: continue
        candidate = os.path.join(dirpath,filename)
        if candidate not in usedFigurePaths:
            os.remove(candidate)
            # print "Delete",candidate
            nDel+=1
        else:
            # print "Delete"
            nSave+=1

print "N Delete", nDel
print "N Save", nSave
