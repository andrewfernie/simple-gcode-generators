import sys
import math
import time
from Tkinter import *

class Application(Frame):

	def __init__(self, master=None):
		Frame.__init__(self,master)
		self.grid()
		self.createwidgets()
		self.defaultpara()
		
	def createwidgets(self):
		self.title = Label(self, text='Helical Boring G-Code')
		self.title.grid(row=0,column=0,columnspan=4)
		
		######OPTIONS
		self.optionsL = Label(self, text='Options')
		self.optionsL.grid(row=1,column=0,columnspan=2)
		
		self.finish = IntVar()
		self.finishB = Checkbutton(self, text='Finish Pass', variable=self.finish, onvalue=1, offvalue=0)
		self.finishB.grid(row=2,column=0,columnspan=2)
		
		self.finishpass = StringVar()
		self.finishpassL = Label(self, text='Finish Pass Amount')
		self.finishpassL.grid(row=3,column=0)
		self.finishpassE = Entry(self, textvariable=self.finishpass, width=10)
		self.finishpassE.grid(row=3,column=1)
		
		self.spindle = IntVar()
		self.spindleB = Checkbutton(self, text='Turn on Spindle', variable=self.spindle, onvalue=1,offvalue=0)
		self.spindleB.grid(row=4,column=0,columnspan=2)
		
		self.coolant = IntVar()
		self.coolantB = Checkbutton(self, text='Coolant', variable=self.coolant, onvalue=1, offvalue=0)
		self.coolantB.grid(row=5,column=0,columnspan=2)
		
		#######TOOLS
		self.Tool = Label(self, text='Tool')
		self.Tool.grid(row=1,column=2,columnspan=2)
		
		self.toold = StringVar()
		self.tooldL = Label(self, text='Tool Diameter')
		self.tooldL.grid(row=2,column=2)
		self.tooldE = Entry(self, textvariable=self.toold, width=10)
		self.tooldE.grid(row=2,column=3)
		
		self.toolN = StringVar()
		self.toolNL = Label(self, text='Tool Number')
		self.toolNL.grid(row=3,column=2)
		self.toolNE = Entry(self, textvariable=self.toolN, width=10)
		self.toolNE.grid(row=3,column=3)
		
		self.entryA = StringVar()
		self.entryAL = Label(self, text='Max Entry Angle')
		self.entryAL.grid(row=4,column=2)
		self.entryAE = Entry(self, textvariable=self.entryA, width=10)
		self.entryAE.grid(row=4,column=3)
		
		self.MDOC = StringVar()
		self.MDOCL = Label(self, text='Max D.O.C.')
		self.MDOCL.grid(row=5,column=2)
		self.MDOCE = Entry(self, textvariable=self.MDOC, width=10)
		self.MDOCE.grid(row=5,column=3)
		
		self.MWOC = StringVar()
		self.MWOCL = Label(self, text='Max W.O.C.')
		self.MWOCL.grid(row=6,column=2)
		self.MWOCE = Entry(self, textvariable=self.MWOC, width=10)
		self.MWOCE.grid(row=6,column=3)
		
		self.WOCtype = IntVar()
		self.WOCtypes=[('W.O.C. as % of Tool Diameter', 1),('W.O.C. as Decimal',2)]
		
		for text, value in self.WOCtypes:
			self.WOCtypeB = Radiobutton(self, text=text, value=value, variable=self.WOCtype)
			self.WOCtypeB.grid(row=value+6,column=2,columnspan=2)
		
		self.feed = StringVar()
		self.feedL = Label(self, text='Feedrate')
		self.feedL.grid(row=9,column=2)
		self.feedE = Entry(self, textvariable=self.feed, width=10)
		self.feedE.grid(row=9,column=3)
		
		self.speed = StringVar()
		self.speedL = Label(self, text='Spindle Speed')
		self.speedL.grid(row=10,column=2)
		self.speedE = Entry(self, textvariable=self.speed, width=10)
		self.speedE.grid(row=10,column=3)
		
		
		######Hole Parameters
		
		self.holeparam = Label(self, text='Hole Parameters')
		self.holeparam.grid(row=11,column=2,columnspan=2)
		
		self.diameter = StringVar()
		self.diameterL = Label(self, text='Hole Diameter')
		self.diameterL.grid(row=12,column=2)
		self.diameterE = Entry(self, textvariable=self.diameter, width=10)
		self.diameterE.grid(row=12,column=3)
		
		self.depth = StringVar()
		self.depthL = Label(self, text='Hole Depth')
		self.depthL.grid(row=13,column=2)
		self.depthE = Entry(self, textvariable=self.depth, width=10)
		self.depthE.grid(row=13,column=3)
		
		self.rapidh = StringVar()
		self.rapidhL = Label(self, text='Rapid Height')
		self.rapidhL.grid(row=14,column=2)
		self.rapidhE = Entry(self, textvariable=self.rapidh, width=10)
		self.rapidhE.grid(row=14,column=3)
		

			
		self.cpointx = StringVar()
		self.cpointy = StringVar()
		self.cpointz = StringVar()
		
		self.cpointxL = Label(self, text='Centerpoint X')
		self.cpointxL.grid(row=16,column=2)
		
		self.cpointyL = Label(self, text='Centerpoint Y')
		self.cpointyL.grid(row=17,column=2)
		
		self.cpointzL = Label(self, text='Centerpoint Z')
		self.cpointzL.grid(row=18,column=2)
		
		self.cpointxE = Entry(self, textvariable=self.cpointx, width=10)
		self.cpointxE.grid(row=16,column=3)
		
		self.cpointyE = Entry(self, textvariable=self.cpointy, width=10)
		self.cpointyE.grid(row=17,column=3)
		
		self.cpointzE = Entry(self, textvariable=self.cpointz, width=10)
		self.cpointzE.grid(row=18,column=3)
		
		#######Cut Parameters
		
		self.CreateB = Button(self, text='Create G-Code',width=20,command=self.createCODE)
		self.CreateB.grid(row=7,column=0)
		
		######PRINTOUT
		
		self.scroll = Scrollbar(self)
		self.scroll.grid(row=1,rowspan=30,column=6,sticky=N+S)
		
		self.textout = Text(self, width=50, height=40, yscrollcommand=self.scroll.set)
		self.textout.grid(row=1,rowspan=30,column=5)
		
		self.scroll.config(command=self.textout.yview)
		
		
	def createCODE(self):
		#Data Pull
		self.fpass = float(self.finishpass.get())
		self.spin = int(self.spindle.get())
		self.cool = int(self.coolant.get())
		self.t_d = float(self.toold.get())
		self.t_n = int(self.toolN.get())
		self.t_a = float(self.entryA.get())
		self.t_doc = float(self.MDOC.get())
		self.fr = float(self.feed.get())
		self.rpm = float(self.speed.get())
		if self.WOCtype.get() == 2:
			self.woc = float(self.MWOC.get())
		else:
			self.woc = ((float(self.MWOC.get()))*.01)* (self.t_d)
		self.dia = float(self.diameter.get())
		self.dep = float(self.depth.get())
		self.r_z = float(self.rapidh.get())
		
		self.in_x = self.cpointx.get()
		self.in_y = self.cpointy.get()
		self.in_z = self.cpointz.get()
		
		self.sp_x = self.in_x.split(',')
		self.sp_y = self.in_y.split(',')
		self.sp_z = self.in_z.split(',')
		
		self.h_n = len(self.in_x.split(','))
		self.h_ny = len(self.in_y.split(','))
		self.h_nz = len(self.in_z.split(','))
		self.coord = 1
		self.count = IntVar()
		self.count = 0
		#######CALCULATIONS
		
		self.h_N = (self.h_n == self.h_ny) and (self.h_ny == self.h_nz)
		
		if not self.h_N:
		
			self.textout.delete('1.0',END)
			self.textout.insert(INSERT,'UNEQUAL NUMBER OF COORDINATES GIVEN')
			self.textout.insert(INSERT,'\n# of X = %s'%(self.h_n))
			self.textout.insert(INSERT,'\n# of Y = %s'%(self.h_ny))
			self.textout.insert(INSERT,'\n# of Z = %s'%(self.h_nz))
			
			return
			
		
		self.t_r = self.t_d * .5
		
		self.f_d = self.dia
		self.f_r = (self.dia * .5)-(self.t_r)
	
		if self.finish.get() == 1:
			self.r_d = self.dia - (self.fpass*2)
			self.r_r = (self.r_d*.5)-(self.t_r)
		
			if self.r_r <= 0:
				
				self.textout.delete('1.0',END)
				self.textout.insert(INSERT,'FINISH PASS TOO LARGE')
				
				return
		
		else: 
			self.r_d = self.dia
			self.r_r = (self.dia *.5)-(self.t_r)
		
		self.E_r = self.t_r * .90
			
		if self.E_r >= self.r_r:
				
			self.e_r = self.r_r
				
		else:
			self.e_r = self.E_r
		
		if self.woc > self.t_d :
		
			self.textout.delete('1.0',END)
			self.textout.insert(INSERT,'W.O.C. LARGER THAN TOOL DIAMETER')
			
			return
		
		
		######WRITE CODE
		###TOOL 
		self.textout.delete('1.0',END)
		
		###SPINDLE PARA
		
		self.textout.insert('1.0', 'M06 T%d' %(self.t_n))

		if self.spin == 1:
			self.textout.insert(INSERT,'\nM03 S%s' %(self.rpm))
			
		if self.cool == 1:
			self.textout.insert(INSERT,'\nM08')
			
		####RAPID Z
		
		self.textout.insert(INSERT, '\nG00 Z%s' %(self.r_z))

		###Rapid X,Y
		

		while self.coord <= self.h_n:
			
			exec 'self.c_x%s = self.sp_x[int(self.count)]'%(self.coord)
			exec 'self.c_y%s = self.sp_y[int(self.count)]'%(self.coord)
			exec 'self.c_z%s = self.sp_z[int(self.count)]'%(self.coord)
				
			exec 'self.circleCode(self.c_x%s,self.c_y%s,self.c_z%s)'%(self.coord,self.coord,self.coord)
				
			self.coord += 1
			self.count += 1
				
	def circleCode(self,c_x,c_y,c_z):
		
		self.c_x = float(c_x)
		self.c_y = float(c_y)
		self.c_z = float(c_z)
		
		if self.c_z >= self.r_z :
		
			self.textout.delete('1.0',END)
			self.textout.insert(INSERT,'RAPID Z HEIGHT BENEATH Z CENTERPOINT')
			
			return
	
		self.f_z = (self.c_z)-(self.dep)		
		if self.f_z <= (self.c_z-self.t_doc):
		
			self.i_z = (self.c_z)-(self.t_doc)
			
		else:
		
			self.i_z = self.f_z
		
		
		self.s_x = (self.c_x) - self.e_r
		self.s_y = self.c_y
		self.s_z = self.c_z + .005
		
		self.s_cir = (self.e_r*2)*math.pi
		self.s_dz = (self.s_cir)*math.sin((math.radians(self.t_a)))
		self.s_nz = (self.s_z)-(self.s_dz)
		
		
		#####RAPID X Y
		self.textout.insert(INSERT,'\nG00 X%s Y%s' %((round(self.s_x, 4)),(round(self.s_y))))
			
		#####Feed to Z
			
		self.textout.insert(INSERT,'\nG01 Z%s F%s' %((round(self.s_z,4)),(round(self.fr,4))))
			
		#####Circle Cutting
		while self.i_z >= self.f_z:
			
		#####DIA CHECK
			
			if self.t_d >= self.dia:
				self.textout.delete('1.0',END)
				self.textout.insert(INSERT,'TOOL DIAMETER TOO LARGE')
				return
			
			#####Spiral Plunge
			self.textout.insert(INSERT,'\nG01 X%s Y%s'%((round(self.s_x,4)),(round(self.s_y))))
			while self.s_nz >= self.i_z:
				
				self.textout.insert(INSERT,'\nG03 I%s Z%s' %((round(self.e_r,4)),(round(self.s_nz, 4))))
				
				self.s_nz -= self.s_dz
				
			self.textout.insert(INSERT,'\nG03 I%s Z%s' %((round(self.e_r,4)),(round(self.i_z,4))))
			
				
			self.n_r = self.e_r + self.woc
					
			while self.n_r <= self.r_r:
				self.n_x = self.c_x - self.n_r
				self.textout.insert(INSERT,'\nG01 X%s Y%s'%((round(self.n_x,4)),(round(self.s_y,4))))
				self.textout.insert(INSERT,'\nG03 I%s'%((round(self.n_r,4))))
						
				self.n_r += self.woc
			self.r_x = (self.c_x)-(self.r_r)
			self.textout.insert(INSERT,'\nG01 X%s Y%s'%((round(self.r_x,4)),(round(self.s_y,4))))
			self.textout.insert(INSERT,'\nG03 I%s'%(round(self.r_r,4)))
			
			if self.i_z == self.f_z:
				break
			####END OF LOOP
			self.i_z -= self.t_doc
			if self.f_z > self.i_z:
				self.i_z = self.f_z
				
		if self.finish.get() == 1:
			self.f_x = (self.c_x)-(self.f_r)
			self.textout.insert(INSERT,'\nG01 X%s Y%s'%((round(self.f_x,4)),(round(self.s_y,4))))
			self.textout.insert(INSERT,'\nG03 I%s'%(round(self.f_r,4)))
				
		self.textout.insert(INSERT,'\nG00 Z%s'%(round(self.r_z,4)))
		
		
		
		
		
		
		
	def defaultpara(self):
		self.finish.set(1)
		self.WOCtype.set(2)
		self.toold.set(.25)
		self.MWOC.set(.125)
		self.finishpass.set(.005)
		self.toolN.set(2)
		self.entryA.set(2)
		self.MDOC.set(.125)
		self.diameter.set(1.125)
		self.depth.set(.25)
		self.rapidh.set(.125)
		self.cpointx.set(0)
		self.cpointy.set(0)
		self.cpointz.set(0)
		self.speed.set(3500)
		self.feed.set(10)
	

App = Application()
App.master.title('Helical Boring G-Code')
App.mainloop()

"""		
ALEC SIMPSON
09/23/12
"""
