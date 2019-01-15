#!/usr/bin/env python2

# This tool is designed to take a URL arguement, and return a password via xdotool. It's a plugin
# for vimb
#

# Syntax:
# passwordTool.py [line] [url]
# Where line is the line number requested from pass, and url is the full url which will be stripped
# down to a domain+tld for pass

# Requires linux tools: xdotool, pass

import os, sys, time

def notify(s):
    global timeout
    os.popen('notify-send -t {0} "{1}"'.format(timeout*1000,s))

def loadInputs():
    global lastAccessPath, timeout

    # decide mode based on last access
    lastAccess = getLastAccess(lastAccessPath)
    print time.time(), lastAccess,time.time()-lastAccess ,timeout, time.time()-lastAccess > timeout
    if time.time()-lastAccess > timeout:
        mode=0
        notify("Sending username. 10s to send password")
    else:
        mode=1
        notify("Sending password. password for next 10s")

    # check inputs
    if len(sys.argv)<3:
        print "="*50
        print "sys.argv:",sys.argv
        print "="*50
        raise BaseException("Incorrect number of arguements")
    # parse
    url  = sys.argv[2]
    oPath = sys.argv[1]
    xid = None
    return mode,url,xid,oPath

def parseUrl(url):
    # parse the url to return just the domain
    if len(url.split("."))<2:
        raise BaseException("Not enough dots in url")
    # remove any protocol
    url = url.replace("https://","")
    url = url.replace("http://","")
    url = url.replace("ftp://","")
    # ensure there's a slash
    url = url+"/"
    # get first part
    url = url.split("/")[0]
    # get domain and tld (last two dot seperated strings)
    url = ".".join(url.split(".")[-2:])
    return url

def lookupPass(domain,mode):
    # call pass to look domain
    global resorucePath
    command = "pass {0}/{1}".format(resorucePath,domain)
    passResult = os.popen(command).readlines()
    if len(passResult)<mode:
        raise BaseException("Two few lines found in pass file")
    return passResult[mode]

# def xdoWrap(string,xid=None):
#     # xdotool the string
#     if xid!=None:
#         command = "xdotool type --window {0} --clearmodifiers {1}".format(string,xid)
#     else:
#         command = "xdotool type --clearmodifiers {0}".format(string)
#     os.popen(command)

def debug(*string):
    # Print debug string, if verbose is on
    global verbose
    string = [str(s) for s in string]
    string = " ".join(string)
    if verbose:
        print ("DEBUG: {0}".format(string))

def pipeOutput(data,oPath):
    # Save data to oPath
    f = open(oPath,"w")
    f.write(data)
    f.close()

def getLastAccess(lastAccessPath):
    # get last access time
    if not os.path.isfile(lastAccessPath):
        # create new file
        ret = 0
        open(lastAccessPath,"w").write(str(time.time()))
    else:
        ret = open(lastAccessPath,"r").read()
        open(lastAccessPath,"w").write(str(time.time()))
    return float(ret)


# customization: pass directory where website info is saves
lastAccessPath = "/home/prime/.passWordToolAccess"
timeout = 10
resorucePath = "web"
verbose = False

mode,url,xid,oPath = loadInputs()
# url = "cern.ch" # temporary over-ride for testing
debug("running with", mode, url)
domain = parseUrl(url)
debug("domain", domain)
data = lookupPass(domain,mode)
debug("found data", data)
pipeOutput(data,oPath)
