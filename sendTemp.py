#! /bin/env python2

##################################################
# Script to send temp info to usb
# Init via udev rule
# Quits when it can't find the usb device
##################################################

from __future__ import division
import os, json, random, glob, time
import serial 

def getTemp():
    """ get temperatuire """
    f= os.popen("sensors -j").readlines()
    f = json.load(os.popen("sensors -j"))
    temps= [f[u"coretemp-isa-0000"]["Core {0}".format(i)]["temp{0}_input".format(i+2)] for i in range(8)]
    temp=sum(temps)/len(temps)
    return "{0:.1f}".format(temp)

    # t1 = f["pch_skylake-virtual-0"]["temp1"]["temp1_input"]
    # t2 = f["coretemp-isa-0000"]["Package id 0"]["temp1_input"]
    # return "{0:.1f}".format((t1+t2)/2)


# 0403:6001
paths = "/sys/bus/usb-serial/devices/ttyUSB*/../uevent"
devPath=None
for p in glob.glob(paths):
    cmd = "grep PRODUCT= {0}".format(p)
    result=os.popen(cmd).read()[:-1]
    print p
    print result
    target="PRODUCT=1a86/7523/254"
    if result==target:
        serialName = p.split("/")
        print "Got serial name for arduino", serialName
        devPath = "/dev/{0}".format(serialName[5])
        break
if devPath==None:
    print "Didn't find connected arduino path"
    quit()

def exists(devPath):
    """ Tries to locate USB several times """
    nTrys=10
    for i in range(nTrys):
        if os.path.exists(devPath):
            return True
        print "Didn't find {0} time".format(i)
        time.sleep(10)
    return False

# devPath = "/dev/ttyUSB0"

# os.popen("stty -F {0} ispeed 9600 ospeed 9600 -hupcl".format(devPath))
# os.popen("stty -F {0} ispeed 9600 ospeed 9600 -ignpar cs8 -cstopb -echo".format(devPath))
os.popen("stty -F {0} 9600 -cstopb".format(devPath))


ser = serial.Serial(devPath)
time.sleep(1)

while exists(devPath):
    send = "{0}\\n".format(getTemp())
    print "Writing",send
    os.popen("echo {0} c > {1} ".format(send,devPath))
    time.sleep(2)


ser.close()
