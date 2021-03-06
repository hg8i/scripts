#!/usr/bin/env python3

import gi, os, time
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.Gdk import Color

def run(c):
    """ Verbose popen wrapper """
    print("Running:")
    print(c)
    return os.popen(c)

class MyStatusIconApp:
    def __init__(self,protected):
        self.protected=protected # protected, unmountable if this is in blockName
        self.status_icon = Gtk.StatusIcon()
        picturePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pic.png")
        self.status_icon.set_from_file(picturePath)
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.status_icon.connect("activate", self.left_click_event)
        self.blockData={} # block data
        # colors
        x = 40000
        self.protectedFgColor = Color(x,x,x)
        self.normalFgColor = Color(0,x,0)

        self.button = Gtk.Button(label="Click Here")
        self.buttonConnect= self.button.connect("clicked", lambda x: print("button"))

    def parseUdisk(self, block):
        """ Return dictionary of information about /dev/{block} """
        # get detailed udisk info
        udisk = run("udisksctl info -b /dev/{0}".format(block)).readlines()
        # only take entries with ":" and defined field
        udisk = [s[:-1].replace(" ","") for s in udisk if len(s.split(":"))==2]
        # parse to dictionary
        udisk = {s.split(":")[0]:"".join(s.split(":")[1:]) for s in udisk}
        # also add block address
        udisk["name"] = block
        udisk["blockPath"] = "/dev/"+block
        return udisk


    def getListOfDrives(self,mountedOnly=True):
        """ Get a list of mounted drives, save as self.blockData """
        # get generic output
        udiskOutput = run("lsblk -n -r").readlines()
        # get mounted blocknames
        blockNames = [s.split()[0] for s in udiskOutput]
        # get detailed info
        self.blockData = [self.parseUdisk(b) for b in blockNames]
        if mountedOnly:
            self.blockData = [b for b in self.blockData if "MountPoints" in b]
            self.blockData = [b for b in self.blockData if b["MountPoints"]!=""]
        # output
        print("Found blocks", blockNames)
        # for block in self.blockData:
        #     if "MountPoints" in block.keys():
        #         print(block["name"], block["MountPoints"])

    def makeMenuList(self,menu,nameFunc,actionFunc):
        """ Add entries of self.blockData to menu
            Labels are based on nameFunc(block)
            Action is actionFunc(block)
        """
        labels=[]
        for block in self.blockData:
            label = Gtk.MenuItem()
            label.set_label(nameFunc(block))
            # if block is protected, change color, don't connect
            if any([p in block["name"] for p in self.protected]):
                label.modify_fg(Gtk.StateFlags.NORMAL,self.protectedFgColor)
            else:
                label.modify_fg(Gtk.StateFlags.NORMAL,self.normalFgColor)
            label.connect("activate", actionFunc, block)
            menu.append(label)

    def unmount(self,x, block):
        """ Unmount block """
        if any([p in block["name"] for p in self.protected]):
            print("No unmount")
            return
        print("Unmount", block["name"])
        run("udisksctl unmount -b {0}".format(block["blockPath"]))
        time.sleep(4)
        run("udisksctl power-off -b {0}".format(block["blockPath"]))
        print("Done")

    def infoLauncher(self,x, block):
        """ Information window popup """
        print("Information on", block["name"])
        win = infoWindow(block)
        win.show_all()


    def left_click_event(self,event):
        """ make popup menu for unmounting """
        self.getListOfDrives(mountedOnly=True)
        nameFunc = lambda block: "Unmount {0} at {1}".format(block["name"],block["MountPoints"])
        # make menu
        self.menu = Gtk.Menu()
        self.makeMenuList(self.menu,nameFunc,self.unmount)
        # add buttons to list
        self.menu.show_all()
        self.menu.popup(None, None, None, self.status_icon, 1, time.time())

    def right_click_event(self, icon, button, time):
        """ make popup menu for additional drive info """
        self.getListOfDrives(mountedOnly=False)
        nameFunc = lambda block: "Information on {0}".format(block["name"])
        # make menu
        self.menu = Gtk.Menu()
        self.makeMenuList(self.menu,nameFunc,self.infoLauncher)
        # add buttons to list
        self.menu.show_all()
        self.menu.popup(None, None, None, self.status_icon, 1, time)

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("StatusIcon Example")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Andrew Steele"])

        about_dialog.run()
        about_dialog.destroy()

# popup window
class infoWindow(Gtk.Window):
    def __init__(self,block):
        self.block = block
        Gtk.Window.__init__(self, title="Hello World")
        Gtk.Window.set_modal(self,1)
        self.set_default_size(500,500)

        # color
        x = 50000
        self.textBg = Color(x,x,x)
        self.codeColor = Color(0,0,x)

        # key press
        self.connect("key-press-event", self.keyPress)
        self.drawInfo()

    def keyPress(self, widget, ev, data=None):
        # if ev.keyval == Gdk.KEY_Escape: #If Escape pressed, reset text
        if ev.keyval == Gdk.KEY_q: #If Escape pressed, reset text
            self.destroy()

    def getUUID(self):
        """ Get UUID of rel block, return true if found """
        ls = run("lsblk -fnr").readlines()
        for line in ls:
            if line.split()[0]==self.block["name"]:
                self.uuid = line.split()[2]
                return True
        return False

    def getSerial(self):
        """ Get serial number of rel block, return true if found 
            Assumes serial number is first serial number? Seems okay
        """
        ls = run("udevadm info -a -n {0}".format(self.block["blockPath"])).readlines()
        for line in ls:
            if "serial" in line: 
                if len(line.split('"'))<2: continue
                self.serial=line.split('"')[1]
                return True
        return False


    def drawInfo(self):
        """ Add info to window """
        notebook = Gtk.Notebook()

        #############################################
        #### Info page
        #############################################
        label   = Gtk.Label(label="Information", halign=Gtk.Align.START)
        grid = Gtk.Grid.new()
        self.makeLabel(grid,0,"<big><u><b>Output of: udisksctl info -b /dev/{0}</b></u></big>\n".format(self.block["blockPath"]),width=2,col=0,fgColor=None,wrap=None)
        for i,k in enumerate(self.block.keys()):
             i+=1
             self.makeLabel(grid,i,"<b>{0}</b>".format(k),col=0,align=Gtk.Align.START)
             self.makeLabel(grid,i,self.block[k],col=1,align=Gtk.Align.START,fgColor=self.codeColor,wrap=True,select=True)
        #
        notebook.append_page(grid,label)


        #############################################
        ### Instructions page
        #############################################
        grid = Gtk.Grid.new()
        label   = Gtk.Label(label="Instructions", halign=Gtk.Align.START)
        c1   = "\n<big><b><u>Instructions for setting up mounting</u></b></big>\n"
        c2   = "<big><b>To implement the automatic mounting script</b></big>\n"
        c3   = "Edit (or create) the file /etc/udev/rules.d/50-harddrive.rules and add the following line:\n <tt></tt>"
        self.getSerial()
        if self.getSerial():
            c4   = 'ACTION=="add",KERNEL=="sd[b-z]",ATTRS{{serial}}=="{0}",ENV{{DISPLAY}}=":0",ENV{{XAUTHORITY}}="/home/prime/.Xauthority",RUN+="/usr/bin/su prime -c \"/home/prime/scripts/mountUsb.sh mount petitBox %k\""'.format(self.serial)
            c4  += 'ACTION=="remove",KERNEL=="sd[b-z]",ATTRS{{serial}}=="{0}",ENV{{DISPLAY}}=":0",ENV{{XAUTHORITY}}="/home/prime/.Xauthority",RUN+="/usr/bin/su prime -c \"/home/prime/scripts/mountUsb.sh unmount petitBox %k\""'.format(self.serial)
        else:
            c4   = "<tt>Problem making command (this is probably a partition), run udevadm info -a -n {0}, find a suitable identifier, and follow the instructions in the info page for the main block (ie if this is sda1, look at sda)</tt>".format(self.block["blockPath"])
        c5   = "\n<big><b>To specify the default mounting location of a drive</b></big>\n"
        c6   = "You can change the fstab configuration, edit /etc/fstab and add the line (replacing the path):\n"
        if self.getUUID():
            c7   = "<tt>UUID=5915{0} /HOME/PATH/TO/MOUNT auto nofail,x-systemd.device-timeout=1 0 2</tt>\n".format(self.uuid)
        else:
            c7   = "<tt>Problem making command, edit /etc/fstab</tt>"
        c8 = "You may also need to enable unauthenticated unmounting. See https://askubuntu.com/questions/552503/stop-asking-for-authentication-to-mount-usb-stick"

        #
        self.makeLabel(grid,0,c1, align=Gtk.Align.START)
        self.makeLabel(grid,1,c2, align=Gtk.Align.START)
        self.makeLabel(grid,2,c3, align=Gtk.Align.START)
        self.makeLabel(grid,3,c4, wrap=True,fgColor=self.codeColor,select=True)
        self.makeLabel(grid,4,c5, align=Gtk.Align.START)
        self.makeLabel(grid,5,c6, align=Gtk.Align.START)
        self.makeLabel(grid,6,c7, wrap=True,fgColor=self.codeColor,select=True)
        self.makeLabel(grid,7,c8, align=Gtk.Align.START)
        #
        notebook.append_page(grid,label)

        #############################################
        ### About page
        #############################################
        grid = Gtk.Grid.new()
        label   = Gtk.Label(label="About", halign=Gtk.Align.START)
        notebook.append_page(grid,label)
        self.makeLabel(grid,0,"\n<big><b>Mount Manager</b></big>\n2018, CERN")
        self.makeLabel(grid,1,"\n\n====\n\nAaron White\naaronsw@umich.edu")

        self.add(notebook)

    def makeLabel(self,grid,i,s,col=0,width=1,align=None,fgColor=None,wrap=None,select=False):
        l = Gtk.Label.new(s)
        l.set_hexpand(True)
        Gtk.Label.set_use_markup(l,True)
        if align: l.set_halign(align)
        if fgColor: l.modify_fg(Gtk.StateFlags.NORMAL,fgColor)
        if wrap: l.set_line_wrap(True)
        if select: l.set_selectable(True)
        grid.attach(l,col,i,width,1)
        return l

# for testing
# block = {'/org/freedesktop/UDisks2/block_devices/sdc': '', 'org.freedesktop.UDisks2.Block': '', 'CryptoBackingDevice': "'/'", 'Device': '/dev/sdc', 'DeviceNumber': '2080', 'Drive': "'/org/freedesktop/UDisks2/drives/WD_My_Passport_25E1_575847314131374A34523959'", 'HintAuto': 'true', 'HintIconName': '', 'HintIgnore': 'false', 'HintName': '', 'HintPartitionable': 'true', 'HintSymbolicIconName': '', 'HintSystem': 'false', 'IdLabel': '', 'IdType': 'ext4', 'IdUUID': '591542f5-676e-4233-a266-15ad3642d6bc', 'IdUsage': 'filesystem', 'IdVersion': '1.0', 'MDRaid': "'/'", 'MDRaidMember': "'/'", 'PreferredDevice': '/dev/sdc', 'ReadOnly': 'false', 'Size': '1000170586112', 'UserspaceMountOptions': '', 'org.freedesktop.UDisks2.Filesystem': '', 'MountPoints': '/home/prime/petitBox', 'name': 'sdc', 'blockPath': '/dev/sdc'}
# win = infoWindow(block)
# win.connect("destroy", Gtk.main_quit)
# win.show_all()

protected=["sda"]
app = MyStatusIconApp(protected)

Gtk.main()
