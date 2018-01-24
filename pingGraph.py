import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import os,time,random

def getPing():
  f=os.popen("ping -c 1 www.google.com").readlines()
  f1=f[1].split()[-2]
  f2=f1.split("=")
  f3=float(f2[1])
  return f3

def getTime():
  return time.time()

fig, (ax1,ax2) = plt.subplots(2,1)
memSize=1000
#x = np.arange(0, memSize, 1)
x = [getTime()]*memSize
y = [getPing()]*memSize
maxX=[getTime()]
maxY=[]
maxXVal=getTime()
maxYVal=getPing()
lineAllVals, = ax2.plot(x, y,"r,-")
lineMaxVals, = ax1.plot(maxY,maxY,"b.")
historicMaxValue=getPing()
globalCount=0
maxValBins=100
failedState=[0,0]

def animate(i):
  global x,y,historicMaxValue,globalCount,maxX,maxY,maxYVal
  globalCount+=1
  try:
    xvalStart=getTime()
    yval=getPing()
    xvalEnd=getTime()
    xvalEnd=xvalStart+yval/1000
    maxYVal=max(maxYVal,yval)
  except:
    print "failed"
    failedState[0]=1
    return lineAllVals,
  #every N runs, plot max
  if globalCount%maxValBins==0:
    maxY.append(maxYVal)
    maxX.append(xvalEnd)
    if failedState==[0,0]:
      ax1.plot([maxX[-1],maxX[-2]],[maxYVal,maxYVal],"b,-")
      ax1.set_ylim(0.9*min(maxY),1.1*max(maxY))
      ax1.set_xlim(min(maxX),max(maxX))
      maxYVal=yval
    failedState[1]=failedState[0]# shift failed register
    failedState[0]=0
    
  y=np.append(y[1:len(y)],[yval])
  y=np.append(y[1:len(y)],[yval])
  x=np.append(x[1:len(x)],[xvalStart])
  x=np.append(x[1:len(x)],[xvalEnd])
  #print y
  lineAllVals.set_ydata(y)  # update the data
  lineAllVals.set_xdata(x)  # update the data
  time.sleep(1.0)
  historicMaxValue=max(historicMaxValue,max(y))
  historicMaxValue*=0.999
  ax2.set_ylim(0.9*min(y),1.1*historicMaxValue)
  ax2.set_xlim(min(x),max(x))
  return lineAllVals,

def init():
    lineAllVals.set_ydata(np.ma.array(x, mask=True))
    return lineAllVals,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init, interval=25, blit=False)

plt.show()

