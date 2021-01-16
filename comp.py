#!/bin/env python2
import sys,numpy,os

# add values in quadrature, put in clip

p = float(sys.argv[1])
r = float(sys.argv[2])
n = 1
t = float(sys.argv[3])

comb = p*(1+r/n)**(n*t)
comb = "{:,.2f}".format(comb)

print "After ",comb
