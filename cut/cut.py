#!/usr/bin/env python
version = '1.0.0'
# python cut.py
# December 1, 2020
# Cut G-Code Generator for LinuxCNC
"""

    Adapted from face.py by Andrew Fernie. Same rights as provided with face.py described below.

    Copyright (C) <2008>  <John Thornton>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    e-mail me any suggestions to "jet1024 at semo dot net"
    If you make money using this software
    you must donate $20 USD to a local food bank
    or the food police will get you! Think of others from time to time...
    To make it a menu item in Ubuntu use the Alacarte Menu Editor and add 
    the command python YourPathToThisFile/cut.py
    make sure you have made the file execuatble by right
    clicking and selecting properties then Permissions and Execute

    To use with LinuxCNC see the instructions at: 
    https://github.com/linuxcnc/simple-gcode-generators


"""

from Tkinter import *
from tkFileDialog import *
from math import *
from SimpleDialog import *
from ConfigParser import *
from decimal import *
import tkMessageBox
import os


IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width=700, height=400, bd=1)
        self.grid()
        self.createMenu()
        self.createWidgets()
        self.LoadPrefs()


    def createMenu(self):
        #Create the Menu base
        self.menu = Menu(self)
        #Add the Menu
        self.master.config(menu=self.menu)
        #Create our File menu
        self.FileMenu = Menu(self.menu)
        #Add our Menu to the Base Menu
        self.menu.add_cascade(label='File', menu=self.FileMenu)
        #Add items to the menu
        self.FileMenu.add_command(label='New', command=self.ClearTextBox)
        self.FileMenu.add_command(label='Open', command=self.Simple)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Quit', command=self.quit)
        
        self.EditMenu = Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.EditMenu)
        self.EditMenu.add_command(label='Copy', command=self.CopyClpBd)
        self.EditMenu.add_command(label='Select All', command=self.SelectAllText)
        self.EditMenu.add_command(label='Delete All', command=self.ClearTextBox)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label='Save Preferences', command=self.SavePrefs)
        self.EditMenu.add_command(label='Load Preferences', command=self.LoadPrefs)
        
        self.HelpMenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.HelpMenu)
        self.HelpMenu.add_command(label='Help Info', command=self.HelpInfo)
        self.HelpMenu.add_command(label='About', command=self.HelpAbout)

    def createWidgets(self):
        
        self.sp1 = Label(self)
        self.sp1.grid(row=0)
        
        self.st1 = Label(self, text='Cut Length *')
        self.st1.grid(row=1, column=0, sticky=E)
        self.CutLengthVar = StringVar()
        self.PartLength = Entry(self, width=10, textvariable=self.CutLengthVar)
        self.PartLength.grid(row=1, column=1, sticky=W)
        self.PartLength.focus_set()

        self.st6 = Label(self, text='Depth of Each Cut ')
        self.st6.grid(row=2, column=0, sticky=E)
        self.DepthOfCutVar = StringVar()
        self.DepthOfCut = Entry(self, width=10, textvariable=self.DepthOfCutVar)
        self.DepthOfCut.grid(row=2, column=1, sticky=W)

        self.st5 = Label(self, text='Amount to Remove *')
        self.st5.grid(row=3, column=0, sticky=E)
        self.TotalToRemoveVar = StringVar()
        self.TotalToRemove = Entry(self, width=10, textvariable=self.TotalToRemoveVar)
        self.TotalToRemove.grid(row=3, column=1, sticky=W)
        
        self.st10 = Label(self, text='Safe Z height')
        self.st10.grid(row=4, column=0, sticky=E)
        self.SafeZVar = StringVar()
        self.Leadin = Entry(self, width=10, textvariable=self.SafeZVar)
        self.Leadin.grid(row=4, column=1, sticky=W)

        CutAlongOptions=[('X Cut',0),('Y Cut',1)]
        self.CutAlongVar=IntVar()
        for text, value in CutAlongOptions:
            if(value == 0):
                Radiobutton(self, text=text,value=value,
                    variable=self.CutAlongVar,indicatoron=0,width=6,)\
                    .grid(row=5, column=value, sticky = E)
            else:
                Radiobutton(self, text=text,value=value,
                    variable=self.CutAlongVar,indicatoron=0,width=6,)\
                    .grid(row=5, column=value, sticky = W)

        self.CutAlongVar.set(0)
        
        self.st3 = Label(self, text='Tool Diameter ')
        self.st3.grid(row=1, column=2, sticky=E)
        self.ToolDiameterVar = StringVar()
        self.ToolDiameter = Entry(self, width=10, textvariable=self.ToolDiameterVar)
        self.ToolDiameter.grid(row=1, column=3, sticky=W)
        
        self.st4 = Label(self, text='Feedrate ')
        self.st4.grid(row=2, column=2, sticky=E)
        self.FeedrateVar = StringVar()
        self.Feedrate = Entry(self, width=10, textvariable=self.FeedrateVar)
        self.Feedrate.grid(row=2, column=3, sticky=W)

        self.st4a = Label(self, text='M3 Spindle RPM ')
        self.st4a.grid(row=3, column=2, sticky=E)
        self.SpindleRPMVar = StringVar()
        self.SpindleRPM = Entry(self, width=10, textvariable=self.SpindleRPMVar)
        self.SpindleRPM.grid(row=3, column=3, sticky=W)
                
        self.st8 = Label(self, text='Lead In / Lead Out')
        self.st8.grid(row=4, column=2, sticky=E)
        self.LeadinVar = StringVar()
        self.Leadin = Entry(self, width=10, textvariable=self.LeadinVar)
        self.Leadin.grid(row=4, column=3, sticky=W)

        
        self.spacer3 = Label(self, text='')
        self.spacer3.grid(row=6, column=0, columnspan=4)
        
        self.g_code = Text(self,width=30,height=30,bd=3)
        self.g_code.grid(row=7, column=0, columnspan=5, sticky=E+W+N+S)
        self.tbscroll = Scrollbar(self,command = self.g_code.yview)
        self.tbscroll.grid(row=7, column=5, sticky=N+S+W)
        self.g_code.configure(yscrollcommand = self.tbscroll.set) 

        self.sp4 = Label(self)
        self.sp4.grid(row=8)
        
        self.st8=Label(self,text='Units')
        self.st8.grid(row=0,column=5)
        UnitOptions=[('Inch',1),('MM',2)]
        self.UnitVar=IntVar()
        for text, value in UnitOptions:
            Radiobutton(self, text=text,value=value,
                variable=self.UnitVar,indicatoron=0,width=6,)\
                .grid(row=value, column=5)
        self.UnitVar.set(1)
               
        self.st9=Label(self,text='X0-Y0')
        self.st9.grid(row=3,column=5)
        HomeOptions=[('Right-Rear',4),('Left-Front',5)]
        self.HomeVar=IntVar()
        for text, value in HomeOptions:
            Radiobutton(self, text=text,value=value,
                variable=self.HomeVar,indicatoron=0,width=11,)\
                .grid(row=value, column=5)
        self.HomeVar.set(4)
               
        self.GenButton = Button(self, text='Generate G-Code',command=self.GenCode)
        self.GenButton.grid(row=8, column=0)
        
        self.CopyButton = Button(self, text='Select All & Copy',command=self.SelectCopy)
        self.CopyButton.grid(row=8, column=1)
        
        self.WriteButton = Button(self, text='Write to File',command=self.WriteToFile)
        self.WriteButton.grid(row=8, column=2)

        if IN_AXIS:
            self.toAxis = Button(self, text='Write to AXIS and Quit',\
                command=self.WriteToAxis)
            self.toAxis.grid(row=8, column=3)
        
            self.quitButton = Button(self, text='Quit', command=self.QuitFromAxis)
            self.quitButton.grid(row=8, column=5, sticky=E)
        else:
            self.quitButton = Button(self, text='Quit', command=self.quit)
            self.quitButton.grid(row=8, column=5, sticky=E)    

    def QuitFromAxis(self):
        sys.stdout.write("M2 (Cut.py Aborted)")
        self.quit()

    def WriteToAxis(self):
        sys.stdout.write(self.g_code.get(0.0, END))
        self.quit()

    def GenCode(self):
        """ Generate the G-Code for cutting a part 
        assume that the part is at X0 to X+, Y0 to Y-"""
        D=Decimal

        # Calculate the start position 1/2 the tool diameter + 0.100 in X and Stepover in Y
        self.ToolRadius = self.FToD(self.ToolDiameterVar.get())/2

       # Calculate the start position 1/2 the tool diameter + 0.100 in X and Stepover in Y
        self.ToolRadius = self.FToD(self.ToolDiameterVar.get())/2
        
        if len(self.LeadinVar.get())>0:
            self.LeadIn = self.FToD(self.LeadinVar.get())
        else:
            self.LeadIn = self.ToolRadius + D('0.1')
        
        self.X_Start = -(self.LeadIn)
        self.X_End = self.FToD(self.CutLengthVar.get()) + self.LeadIn
        
        self.Y_Start = 0.0
        self.Y_End = 0.0
        
        self.Z_Total = self.FToD(self.TotalToRemoveVar.get())
        if len(self.DepthOfCutVar.get())>0:
            self.Z_Step = self.FToD(self.DepthOfCutVar.get())
            self.NumOfZSteps = int(self.FToD(self.TotalToRemoveVar.get()) / self.Z_Step)
            if self.Z_Total % self.Z_Step > 0:
                self.NumOfZSteps = self.NumOfZSteps + 1
        else:
            self.Z_Step = 0
            self.NumOfZSteps = 1

        self.Z_Position = 0
        # Generate the G-Codes
        if self.UnitVar.get()==1:
            self.g_code.insert(END, 'G20\n')                    # inches
        else:
            self.g_code.insert(END, 'G21\n')                    # mm

        self.g_code.insert(END, 'G90\n')                        # Absolute movement mode

        # Set spindle speed and turn it on 
        if len(self.SpindleRPMVar.get())>0:
            self.g_code.insert(END, 'S%i ' %(self.FToD(self.SpindleRPMVar.get())))
            self.g_code.insert(END, 'M3 ')

        # Set Feed rate
        if len(self.FeedrateVar.get())>0:
            self.g_code.insert(END, 'F%s\n' % (self.FeedrateVar.get()))

        # Go to safe Z position
        self.g_code.insert(END, 'G0 Z%s\n' % (self.SafeZVar.get()))

        # Go to start position
        self.g_code.insert(END, 'G0 X%.4f Y%.4f\n' \
                %(self.X_Start, self.Y_Start))

        self.X_Position = self.X_Start

        for i in range(self.NumOfZSteps):

            # Make sure the Z position does not exceed the total depth
            if self.Z_Step>0 and (self.Z_Total+self.Z_Position) >= self.Z_Step:
                self.Z_Position = self.Z_Position - self.Z_Step
            else:
                self.Z_Position = -self.Z_Total

            self.g_code.insert(END, 'G1 Z%.4f\n' % (self.Z_Position))

            if self.X_Position == self.X_Start: 
                self.g_code.insert(END, 'G1 X%.4f\n' % (self.X_End))
                self.X_Position = self.X_End
            else:
                self.g_code.insert(END, 'G1 X%.4f\n' % (self.X_Start))
                self.X_Position = self.X_Start

        # Go to safe Z position
        self.g_code.insert(END, 'G0 Z%s\n' % (self.SafeZVar.get()))
        
        # Go to start position
        self.g_code.insert(END, 'G0 X%.4f Y%.4f\n' \
                %(self.X_Start, self.Y_Start))

        # Turn off spindle
        if len(self.SpindleRPMVar.get())>0:
            self.g_code.insert(END, 'M5\n')

        self.g_code.insert(END, 'M2 (End of File)\n')

    def FToD(self,s): # Float To Decimal
        """
        Returns a decimal with 4 place precision
        valid imputs are any fraction, whole number space fraction
        or decimal string. The input must be a string!
        """
        s=s.strip(' ') # remove any leading and trailing spaces
        D=Decimal # Save typing
        P=D('0.0001') # Set the precision wanted
        if ' ' in s: # if it is a whole number with a fraction
            w,f=s.split(' ',1)
            w=w.strip(' ') # make sure there are no extra spaces
            f=f.strip(' ')
            n,d=f.split('/',1)
            return D(D(n)/D(d)+D(w)).quantize(P)
        elif '/' in s: # if it is just a fraction
            n,d=s.split('/',1)
            return D(D(n)/D(d)).quantize(P)
        return D(s).quantize(P) # if it is a decimal number already

    def GetIniData(self,FileName,SectionName,OptionName,default=''):
        """
        Returns the data in the file, section, option if it exists
        of an .ini type file created with ConfigParser.write()
        If the file is not found or a section or an option is not found
        returns an exception
        """
        self.cp=ConfigParser()
        try:
            self.cp.readfp(open(FileName,'r'))
            try:
                self.cp.has_section(SectionName)
                try:
                    IniData=self.cp.get(SectionName,OptionName)
                except:
                    IniData=default
            except:
                IniData=default
        except:
            IniData=default
        return IniData
        
    def WriteIniData(self,FileName,SectionName,OptionName,OptionData):
        """
        Pass the file name, section name, option name and option data
        When complete returns 'sucess'
        """
        self.cp=ConfigParser()
        try:
            self.fn=open(FileName,'a')
        except IOError:
            self.fn=open(FileName,'w')
        if not self.cp.has_section(SectionName):
            self.cp.add_section(SectionName)
        self.cp.set(SectionName,OptionName,OptionData)
        self.cp.write(self.fn)
        self.fn.close()

    def GetDirectory(self):
        self.DirName = askdirectory(initialdir='/home',title='Please select a directory')
        if len(self.DirName) > 0:
            return self.DirName 
       
    def CopyClpBd(self):
        self.g_code.clipboard_clear()
        self.g_code.clipboard_append(self.g_code.get(0.0, END))

    def WriteToFile(self):
        self.NewFileName = asksaveasfile(initialdir=self.NcDir,mode='w', \
		master=self.master,title='Create NC File',defaultextension='.ngc')
        self.NcDir=os.path.dirname(self.NewFileName.name)
        self.NewFileName.write(self.g_code.get(0.0, END))
        self.NewFileName.close()

    def LoadPrefs(self):
        self.NcDir=self.GetIniData('cut.ini','Directories','NcFiles',os.path.expanduser("~"))
        self.FeedrateVar.set(self.GetIniData('cut.ini','MillingPara','Feedrate','1000'))
        self.DepthOfCutVar.set(self.GetIniData('cut.ini','MillingPara','DepthOfCut','3'))
        self.ToolDiameterVar.set(self.GetIniData('cut.ini','MillingPara','ToolDiameter','10'))
        self.SpindleRPMVar.set(self.GetIniData('cut.ini','MillingPara','SpindleRPM','9000'))
        self.LeadinVar.set(self.GetIniData('cut.ini','MillingPara','Leadin'))
        self.UnitVar.set(int(self.GetIniData('cut.ini','MillingPara','UnitVar','2')))
        self.HomeVar.set(int(self.GetIniData('cut.ini','MillingPara','HomeVar','4')))
        self.CutAlongVar.set(int(self.GetIniData('cut.ini','MillingPara','CutAlongVar','1')))
        self.SafeZVar.set(self.GetIniData('cut.ini','MillingPara','SafeZ','10.0'))
        self.CutLengthVar.set(self.GetIniData('cut.ini','Part','X'))
        self.TotalToRemoveVar.set(self.GetIniData('cut.ini','Part','TotalToRemove'))


    def SavePrefs(self):
        def set_pref(SectionName,OptionName,OptionData):
            if not self.cp.has_section(SectionName):
                self.cp.add_section(SectionName)
            self.cp.set(SectionName,OptionName,OptionData)
        self.cp=ConfigParser()
        self.fn=open('cut.ini','w')
        set_pref('Directories','NcFiles',self.NcDir)
        set_pref('MillingPara','Feedrate',self.FeedrateVar.get())
        set_pref('MillingPara','DepthOfCut',self.DepthOfCutVar.get())
        set_pref('MillingPara','ToolDiameter',self.ToolDiameterVar.get())
        set_pref('MillingPara','SpindleRPM',self.SpindleRPMVar.get())
        set_pref('MillingPara','Leadin',self.LeadinVar.get())
        set_pref('MillingPara','UnitVar',self.UnitVar.get())
        set_pref('MillingPara','HomeVar',self.HomeVar.get())
        set_pref('MillingPara','CutAlongVar',self.CutAlongVar.get())
        set_pref('MillingPara','SafeZ',self.SafeZVar.get())
        set_pref('Part','X',self.CutLengthVar.get())
        set_pref('Part','TotalToRemove',self.TotalToRemoveVar.get())
        self.cp.write(self.fn)
        self.fn.close()
	
    def Simple(self):
        tkMessageBox.showinfo('Feature', 'Sorry this Feature has\nnot been programmed yet.')

    def ClearTextBox(self):
        self.g_code.delete(1.0,END)

    def SelectAllText(self):
        self.g_code.tag_add(SEL, '1.0', END)

    def SelectCopy(self):
        self.SelectAllText()
        self.CopyClpBd()

    def HelpInfo(self):
        SimpleDialog(self,
            text='Required fields are:\n'
            'Cut Length,\n'
            'Amount to Remove,\n'
            'and Feedrate\n'
            'Fractions can be entered in most fields',
            buttons=['Ok'],
            default=0,
            title='User Info').go()
    def HelpAbout(self):
        tkMessageBox.showinfo('Help About', 'Programmed by\n'
            'Big John T (AKA John Thornton)\n'
            'Rick Calder\n'
            'Brad Hanken\n'
            'Aglef Kaiser\n'
            'Version ' + version)




app = Application()
app.master.title('Cutting G-Code Generator Version ' + version)
app.mainloop()

