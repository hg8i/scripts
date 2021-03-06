#!/usr/bin/env python2

# this is a script for manipulating workspaces in i3.
# it is designed to be run with i3 bindsym commands:
#     bindsym Mod4+1 workspace 1
#     bindsym Mod4+Shift+1 move container to workspace 1
#
# what it adds is a persistant state, which allows you to
# use the same i3 bindings in multiple "scopes". this is 
# so I can work on several projects (web,term,vim,etc) at
# once, and still use the same keybindings
#
# The key functions are:
#     * moveToWorkspace(name) move to scope:workspace
#     * sendWindowTo(name) send focused window to scope:workspace
#     * increment/decrement scope: change scope, also go to new workspace
#
# Some other functions are:
#     * resetScopes(), removes scopes from previous sessions,
#         called at the start of an i3 session
#     * reset(), reset to some default workspaces
#     * registerScope(name), add a scope
#     * removeScope(name), delete scope
#     * interpretKeystroke(key,modifiers[]), SIMPLE wrapper
#         that calls an i3-msg command based on inputs
# 
# These are implemented in wsManager class

resourcePath="/home/prime/resources/workspaceScopes.pickle"
import pickle, os, sys
import time


class wsManager:
    def __init__(self):
        #initialize
        self.workspaceNames=[">_","web","ana","stk","ltx","pdf"]
        # self.deliminator="]"
        self.deliminator="~"
        self.data={}
        self.getWorkspaceNames()
        self.safeLoadPickle()
        print "ctor"
        self.printData()

    def __exit__(self):
        #destructor
        self.savePickle()
        pass

    def parseCli(self,args):
        #parse string, run appropriate commands
        print args
        mode=args[0]
        auxArg=0
        if len(args)>1: auxArg=args[1]
        if mode=="sendwindowto":
            self.sendWindowTo(auxArg)
        if mode=="moveto":
            self.moveToWorkspace(auxArg)

        if mode=="decrementmonitor":
            self.decrementMonitor()
        if mode=="incrementmonitor":
            self.incrementMonitor()

        if mode=="decrementworkspace":
            self.decrementWorkspace()
        if mode=="incrementworkspace":
            self.incrementWorkspace()
        if mode=="decrementscope":
            self.incrementScope(increment=-1)
        if mode=="incrementscope":
            self.incrementScope(increment=1)
        if mode=="changescope":
            self.changeScope(auxArg)
        if mode=="removescope":
            self.removeScope(auxArg)
        if mode=="reset":
            self.reset()

    def resetScopes(self):
        #clear memory of previous scopes
        self.data={"scopeList":[],"currentScope":-1,"currentWorkspace":-1}
        self.savePickle()

    def removeScope(self,name):
        #clear memory of previous scopes
        self.data["scopeList"].pop(self.data["scopeList"].index(name))
        self.savePickle()

    def registerScope(self,name):
        #add name to list of scopes
        print "INFO: registering scope: {0}".format(name)
        if name not in self.data["scopeList"]:
            self.data["scopeList"].append(name)

    def changeScope(self,name):
        #change to scope name
        self.registerScope(name)
        print "INFO: changing to scope: {0}".format(name)
        self.data["currentScope"]=self.data["scopeList"].index(name)

    def notify(self,msg):
        #notify-send mes
        os.popen('notify-send --expire-time 500 --urgency=normal "{0}"'.format(msg))

    #####################
    # public functions    #
    #####################

    ## ==================================================
    ## / new features
    ## ==================================================

    def getWorkspaces(self):
        false=0
        true=1
        workspaces = os.popen("i3-msg -t get_workspaces").read()
        workspaces = eval(workspaces)
        return workspaces

    def getNameOfNextWorkspaceOnScreen(self,increment=1):
        """
        This is a standalone function that could later be used in
        the workspace app, but that's for future Aaron
        """
        workspaces=self.getWorkspaces()

        # print len(a[0])
        # get focused output
        focusedWorkspace = filter(lambda x: x["focused"],workspaces)[0]
        focusedOutput = focusedWorkspace["output"]
        focusedName = focusedWorkspace["name"]
        # get list of workspaces on that screen
        workspacesOnScreen= [i for i in workspaces if i["output"]==focusedOutput]
        # find next workspace name
        workspacesOnScreenNames = [i["name"] for i in workspacesOnScreen]
        focusedIndex = workspacesOnScreenNames.index(focusedName)
        nextIndex = (focusedIndex+increment)%len(workspacesOnScreenNames)
        nextName = workspacesOnScreenNames[nextIndex]
        return nextName

    def getNameOfNextMonitorWorkspace(self,increment=1):
        """
        Get name of the focused workspace on next monitor     
        """
        workspaces=self.getWorkspaces()

        # get focused display
        focusedWorkspace = filter(lambda x: x["focused"],workspaces)[0]
        focusedOutput = focusedWorkspace["output"]
        focusedName = focusedWorkspace["name"]

        # get sorted list of displays from xrandr
        displayInfoRaw = filter(lambda x: "connected" in x,os.popen("xrandr -q").readlines())
        displayInfoRaw = [x.replace("primary","") for x in displayInfoRaw]
        displayInfo = {i.split()[0]:int(i.split()[2].split("+")[1]) for i in displayInfoRaw if "disconnected" not in i}
        displayNamesInOrder = sorted(displayInfo.keys(),key=lambda x: displayInfo[x],reverse=0)

        # increment to next output
        focusedOutputIndex = displayNamesInOrder.index(focusedOutput)
        nextOutputIndex = (focusedOutputIndex+increment)%len(displayNamesInOrder)
        nextOutput = displayNamesInOrder[nextOutputIndex]

        # find visible workspace in new output
        visibleWorkspace = filter(lambda x: x["visible"] and x["output"]==nextOutput,workspaces)[0]
        visibleWorkspace = visibleWorkspace["name"]
        return visibleWorkspace

    def incrementMonitor(self):
        # increment Monitor to next on screen
        name = self.getNameOfNextMonitorWorkspace(1)
        i3cmd = "workspace"
        self.executeCommand(i3cmd, name)

    def decrementMonitor(self):
        # decrement Monitor to previous on screen
        name = self.getNameOfNextMonitorWorkspace(-1)
        i3cmd = "workspace"
        self.executeCommand(i3cmd, name)

    def incrementWorkspace(self):
        # increment workspace to next on screen
        name = self.getNameOfNextWorkspaceOnScreen(1)
        i3cmd = "workspace"
        self.executeCommand(i3cmd, name)

    def decrementWorkspace(self):
        # decrement workspace to previous on screen
        name = self.getNameOfNextWorkspaceOnScreen(-1)
        i3cmd = "workspace"
        self.executeCommand(i3cmd, name)


    def incrementScope(self,increment=1):
        # increment scope, 
        # replacing all windows on monitors with one from new scope

        workspaces = self.getWorkspaces()

        # get sorted list of displays from xrandr
        displayInfoRaw = filter(lambda x: "connected" in x,os.popen("xrandr -q").readlines())
        displayInfoRaw = [x.replace("primary","") for x in displayInfoRaw]
        displayInfo = {i.split()[0]:int(i.split()[2].split("+")[1]) for i in displayInfoRaw if "disconnected" not in i}
        displayNamesInOrder = sorted(displayInfo.keys(),key=lambda x: displayInfo[x],reverse=0)

        # get focused display
        focusedWorkspace = filter(lambda x: x["focused"],workspaces)[0]
        focusedOutput = focusedWorkspace["output"]
        focusedName = focusedWorkspace["name"]

        # open("/home/prime/log.txt","w").write(focusedName)

        # find visible workspace in each display
        visibleWorkspaces = filter(lambda x: x["visible"],workspaces)
        print visibleWorkspaces
        visibleNames = {v["output"]:v["name"].split("~")[1] if "~" in v["name"] else  v["name"]for v in visibleWorkspaces}
        # print visibleNames

        #move to scope +1
        self.data["currentScope"]+=increment
        self.data["currentScope"]%=len(self.data["scopeList"])

        # update displays
        for display,name in visibleNames.items():
            name = self.getFullName(name)
            self.executeCommand("workspace",name)

            i3cmd= r"""'[workspace="{}"] move workspace to output "{}"'""".format(name,display)
            self.executeCommand(i3cmd,"")

        time.sleep(0.25)
        curScopeName=self.data["scopeList"][self.data["currentScope"]]
        self.notify("Workspace scope: {0}".format(curScopeName))
        name = self.getFullName(focusedName.split("~")[1])
        self.executeCommand("workspace",name)

    def getFullName(self,wsName):
        template="{0}:{1}{3}{2}"
        scopeNumber=self.data["currentScope"]
        scope=self.data["scopeList"][scopeNumber]
        #sortableHash is used by i3bar to sort workspaces
        sortableHashNumber=100*scopeNumber
        #add value of wsName if in defined list of workspace names
        if wsName in self.workspaceNames: 
            sortableHashNumber+=self.workspaceNames.index(wsName)
        #otherwise, try adding it as a number
        name=template.format(sortableHashNumber,scope,wsName,self.deliminator)
        return name

    # def getFullName(self,
    def runCommandWithArg(self,i3cmd,wsName,run=1):
        #run i3 command "i3cmd" with arguement "wsName"
        if wsName=="": wsName=" "
        name=self.getFullName(wsName)
        # try:
        #     if int(wsName) in range(len(self.workspaceNames),10): sortableHashNumber+=int(wsName)
        # except:
        #     pass
        # name=template.format(sortableHashNumber,scope,wsName,self.deliminator)
        if run: 
            self.executeCommand(i3cmd, name)
            print "Move to:",name
        return name

    def sendWindowTo(self,wsNum):
        #send window to new workspace, without changing workspace
        wsNum=abs(int(wsNum))
        wsName=wsNum
        if wsNum<len(self.workspaceNames):
            wsName=self.workspaceNames[wsNum]
        self.runCommandWithArg("move container to workspace", wsName)

    def moveToWorkspace(self,wsNum):
        #move to workspace: scope:worspaceNum
        #should check input
        wsNum=abs(int(wsNum))
        wsName=wsNum
        if wsNum<len(self.workspaceNames):
            wsName=self.workspaceNames[wsNum]
        self.runCommandWithArg("workspace",wsName)

    #####################
    # private functions #
    #####################

    def executeCommand(self,i3cmd,workspace):
        #execute command
        template="i3-msg {0} {1}"
        cmd=template.format(i3cmd,workspace)
        print "="*50
        print cmd
        print "="*50
        os.popen(cmd)

    def printData(self):
        #print scopeList and currentScope
        print "#"*5, "printing data", "#"*5
        print self.data
        # print self.data["currentScope"]

    def getWorkspaceNames(self):
        #get list of current workspace names
        f=os.popen("i3-msg -t get_workspaces").read()
        false=False
        true=True
        data=eval(f)
        #list of names of workspaces
        self.i3names=[x["name"] for x in data]
        #list of "scope part" of names
        self.i3scopes=[x["name"][:str(x["name"]+self.deliminator).find(self.deliminator)] for x in data]
        #index of the focused worksapce
        for self.i3wsIndex, ws in enumerate(data):
            if ws["focused"]: break
        else: self.i3wsIndex=-1
        #scope name, ws name
        self.i3wsName=self.i3names[self.i3wsIndex]
        if self.deliminator in self.i3wsName: self.i3wsName=self.i3wsName[self.i3wsName.find(self.deliminator)+1:]
        self.i3scopeName=self.i3names[self.i3wsIndex][:str(x["name"]+self.deliminator).find(self.deliminator)]

        print "INFO: self.i3scopes", self.i3scopes
        print "INFO: self.i3names", self.i3names
        print "INFO: current selection:"
        print "INFO: self.i3wsIndex", self.i3wsIndex
        print "INFO: self.i3scopeName", self.i3scopeName
        print "INFO: self.i3wsName", self.i3wsName

    # pickle commands
    def savePickle(self):
        #save pickle list 
        pickle.dump(self.data,open(resourcePath,"w"))

    def safeLoadPickle(self):
        #requires self.names to be workspaces
        #load data from pickle file
        try: self.data= pickle.load(open(resourcePath,"r"))
        except: self.data={"scopeList":[""],"currentScope":0,"currentWorkspace":0}
        #correct if scope number too large
        self.data["currentScope"]=min(len(self.data["scopeList"])-1,self.data["currentScope"])
        #correct if scope no longer exists
        for scope in self.data["scopeList"]:
            if scope not in self.i3scopes:
                print "WARNING: There is an inconsistancy: '{0}' not in i3scopes: {1}".format(scope,self.i3scopes)
        #correct if focused workspace doesn't match currentScope
        i3ExpectedScopeName=self.i3scopeName
        storedScopeName=self.data["scopeList"][self.data["currentScope"]]
        print "INFO: i3ExpectedScopeName: {0} storedScopeName: {1}".format(i3ExpectedScopeName,storedScopeName)
        if i3ExpectedScopeName != storedScopeName:
            print "WARNING: There is an inconsistancy: focused scope '{0}' not matching stored scope: {1}".format(i3ExpectedScopeName,storedScopeName)

    def reset(self):
        #reset to default scopes
        self.resetScopes()
        self.registerScope("l")
        self.registerScope("h")
        self.registerScope("d")
        self.registerScope("c")

ws=wsManager()
ws.parseCli(sys.argv[1:])
ws.printData()
ws.__exit__()
