#! /bin/python2

import sys, os, time

#os.popen("/home/prime/scripts/flashesc");quit()


resourcePath="/home/prime/.clipboard/"
os.popen("mkdir -p "+resourcePath)

memoryPath=os.path.join(resourcePath,".mem")

def getNextFile():
  global resourcePath
  savePath=resourcePath+"clipboard-{0}.txt"
  counter=time.time()
  while os.path.exists(savePath.format(counter)):
    counter+=0.01
  return savePath.format(counter)

def saveClipboardToPath(path):
  global memoryPath
  f=open(path,"w")
  selectedText=os.popen("xclip -o").read()
  f.write(selectedText)
  f.close()

  f=open(memoryPath,"w")
  f.write(path)
  f.close()

def copy():
  clipboardFile=getNextFile()
  saveClipboardToPath(clipboardFile)
  #sync to primary AND clipboard
  os.popen("cat {0} | xsel --primary".format(clipboardFile))
  os.popen("cat {0} | xsel --clipboard".format(clipboardFile))

def paste():
  global memoryPath
  mostRecentPastePath=open(memoryPath,"r").read()
  #sync to primary AND clipboard
  os.popen("cat {0} | xsel --primary".format(mostRecentPastePath))
  os.popen("cat {0} | xsel --clipboard".format(mostRecentPastePath))
  #paste 
  os.popen("xdotool key --clearmodifiers shift+Insert")

##other options for paste functionality:
##(these are slower since use keyboard emulation)
#whatToPaste=open(mostRecentPastePath,"r").read()
#os.popen('''echo -n "{0}" | xvkbd -xsendevent -file - 2>/dev/null'''.format(whatToPaste))
#os.popen("xsel | xvkbd -xsendevent -file - 2>/dev/null")
#os.popen("xdotool type --clearmodifiers "+repr(whatToPaste))
  
def showAll(verbose=False):
  global resourcePath, columns, memoryPath
  count=0
  green="\033[32m{0}\033[0m\033[39m\033[49m"
  red="\033[1m\033[31m{0}\033[0m\033[39m\033[49m"
  bold="\033[1m{0}\033[0m"
  listOfPaths=[]
  for path in sorted(os.listdir(resourcePath)):
    printLine="#"*((columns-len(path)-3)/2)+" "+path+" "
    if verbose:
      print green.format(printLine+"#"*(columns-len(printLine)))
    f=open(os.path.join(resourcePath,path),"r").read()
    print red.format(count),bold.format(f[:100])
    if verbose: print ""
    listOfPaths.append(os.path.join(resourcePath,path))
    count+=1
  # get user selection to copy to past board
  nextCb=raw_input("Enter number to move to clipboard: ")
  try: nextCb=int(nextCb)
  except:
    print "Quitting..."
    quit()
  # update memory file
  f=open(memoryPath,"w")
  f.write(listOfPaths[nextCb])
  f.close()

def help():
  global columns
  #print "#"*columns
  print "\nLONGLIVED CLIPBOARD v 0.1, 06-06-17"
  print "Aaron White, aaronsw@umich.edu"
  print "\nUsage:"
  print "\tlonglivedClipboard.py"
  print "\tlonglivedClipboard.py [arg]"
  print "\nArguments:"
  print "\t[ ]\tno opt\tshow menu to select old clipboard"
  print "\t-h\thelp\tprint this message"
  print "\t-c\tcopy\tcopy x selection"
  print "\t-p\tpaste\tpaste x selection with xdotool"
  print "\n"

#capture mode 
if len(sys.argv)>1:
  arg=sys.argv[1]
else:
  arg="none"

#run output
if arg=="-c" or arg=="copy":
  copy()
elif arg=="-p" or arg=="paste":
  paste()
elif arg=="-h" or arg=="help":
  help()
elif arg=="-t" or arg=="test":
  print "test"
  os.popen("/home/prime/scripts/flashesc")
  pass
elif arg=="-v" or arg=="verbose":
  rows, columns = os.popen('stty size', 'r').read().split()
  columns=int(columns)
  showAll(verbose=True)
else:
  rows, columns = os.popen('stty size', 'r').read().split()
  columns=int(columns)
  showAll()

