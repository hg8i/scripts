#!/bin/env python2
import sys,numpy,os

# add values in quadrature, put in clip

inputs = [float(i)**2 for i in sys.argv[1:]]
comb = numpy.sqrt(numpy.sum(inputs))

print "Added in quadrature",comb
os.popen("echo -n '{0:.3f}' | xclip".format(comb))
