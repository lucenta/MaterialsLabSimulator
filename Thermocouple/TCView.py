'''
Description: This file contains the classes for implementing the thermocouple view.
Author: Andrew Lucentini :-)
'''
import tkinter as tk
from tkinter import ttk
from itertools import cycle
import Misc.Styling as st
from PIL import ImageTk, Image
from Misc.helperFunctions import multiple

"""
Class for creating the thermocouple page
"""
class ThermocoupleView(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent) # Initialize this class as a frame

		# Create and configure main frame
		mainArea = tk.Frame(self, bg = st.MAIN_AREA_BG)
		mainArea.grid(row=0, column=0, sticky="nsew")
		mainArea.grid_propagate(0)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# Create and configure main grids
		grid = tuple([i for i in range(20)])
		mainArea.grid_columnconfigure(grid, weight=1, minsize=50)
		mainArea.grid_rowconfigure(grid, weight=1, minsize=35)

		# Create home Button
		self.homeButton = ttk.Button(mainArea, text="Home")
		self.homeButton.grid(row=0, columnspan=2, sticky='nesw')
		
		# Create title
		label = tk.Label(mainArea, text="Thermocouple Simulator", 
			font=st.LARGE_FONT,
			bg = st.MAIN_AREA_BG,
			fg = st.TITLE_COLOUR)
		label.grid(row=0, column=13, columnspan=7, sticky='nse')

		# Frame to make background for element inputs
		bgInput = tk.Frame(mainArea, bg = st.INPUT_BG)
		bgInput.grid(row=2, column=1, columnspan=11, rowspan=6, sticky="nsew")

		# List box for choosing element 1
		tk.Label(mainArea, text="Metal 1", bg=st.INPUT_BG).grid(row=1, column = 2, columnspan=3, stick='nesw')
		self.element_one = MultiListbox(mainArea, ['Metal', 'Seedback Coeff.'])
		self.element_one.grid(row = 2, column = 1, rowspan=6, columnspan=5, sticky='nesw')

		# List box for choosing element 2
		tk.Label(mainArea, text="Metal 2", bg=st.INPUT_BG).grid(row=1, column = 8, columnspan=3, stick='nesw')
		self.element_two = MultiListbox(mainArea, ['Metal', 'Seedback Coeff.'], width=15)
		self.element_two.grid(row = 2, column = 7, rowspan=6, columnspan=5, sticky='nesw')

		# Create description
		label = tk.Label(mainArea, text="Welcome to the thermocouple emulator! "+
			"In this emulator you will be studying the effects that temperature "+
			"and material selection have on the voltage difference between the two "+
			"nodes of the thermocouple. "+
			"You can adjust the metals for the two nodes using the input boxes to the left. "+
			"You can also adjust the temperature at the junction using the slider at the bottom of the screen!",
			bg = st.INPUT_BG,
			wraplength=250,
			fg = 'black',
			justify='left',
			relief='ridge')
		label.grid(row=2, column=13, rowspan=6, columnspan=6, sticky='nesw')

		# Canvas for thermocouple drawing
		self.height = 315
		self.width = 700
		self.canvas = tk.Canvas(mainArea, bg='lightgrey', height=self.height, width=self.width)
		self.canvas.grid(row = 9, column=3, columnspan=14,  rowspan=9, sticky='nw')
		self.canvas.config()

		# T1 scale
		T1Label = tk.Label(mainArea,font=st.MEDIUM_FONT, bg=st.INPUT_BG, text="T1 (\N{DEGREE SIGN}C)")
		T1Label.grid(row=18, column = 0, rowspan=2,columnspan=2, sticky='news')
		self.T1 = tk.Scale(mainArea, from_=25, to=1200, 
			orient=tk.HORIZONTAL, length = 300, 
			bg=st.INPUT_BG,
			resolution=1)
		self.T1.grid(row=18, column=2, rowspan=2, columnspan=5, sticky='nesw')

		# Draw mac logo
		logoImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"macLogo.png"))
		canvas = tk.Canvas(mainArea, bg=st.MAIN_AREA_BG, width=130, height=71, bd=0, highlightthickness=0, relief='ridge')
		canvas.create_image(130/2,71/2, image=logoImg, anchor = "center")
		canvas.image = logoImg
		canvas.grid(row = 17, column = 17, rowspan=3, columnspan=3)

		# Create thermocouple graphic
		r = 20
		x,y = (40, self.height/2)
		gap_width = 60
		couple_width = 25
		start=self.width/4
		end=self.width*5/8

		# Upper Node
		self.canvas.create_line(
			x,y,
			start,self.height/2-gap_width,
			end,self.height/2-gap_width,
			fill='red', width = couple_width)

		# Lower Node
		self.canvas.create_line(
			x,y,
			start,self.height/2+gap_width,
			end,self.height/2+gap_width,
			fill='blue', width = couple_width)

		# Junction
		self.canvas.create_oval(x-r, y-r, x+r, y+r, fill = "orange")

		# Text for displaying T1
		self.T1_text = self.canvas.create_text(5,self.height-5, anchor="sw", text='')

		# Text for displaying T2
		self.T2_text = self.canvas.create_text(end,self.height-5, anchor="s", text='')

		# Text for displaying metal 1
		self.metal_1_text = self.canvas.create_text(self.width/2-50,self.height/2-gap_width, anchor="center", text='')

		# Text for displaying metal 2
		self.metal_2_text = self.canvas.create_text(self.width/2-50,self.height/2+gap_width, anchor="center", text='', fill = 'white')

		# Create voltmeter
		self.voltmeterImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"voltmeter.png"))
		self.canvas.create_image(end+150,self.height/2, image=self.voltmeterImg)
		self.canvas.image = self.voltmeterImg

		# Create wires
		self.wiresImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"wires.png"))
		self.canvas.create_image(end-12,self.height/2-60, image=self.wiresImg, anchor='nw')
		self.canvas.image = self.wiresImg

		# Text for displaying voltage
		self.voltage_text = self.canvas.create_text(end+185,self.height/2-gap_width, anchor="e", text='')
	
	def populateListboxes(self, data):
		"""
		Populate the list boxes with data
		"""
		self.element_one.add_data(data)
		self.element_two.add_data(data)

	def setT1(self, data):
		"""
		Set T1 text
		"""
		self.canvas.itemconfig(self.T1_text, text='T1 = '+str(round(data,2))+'\N{DEGREE SIGN}C')

	def setT2(self, data):
		"""
		Set T2 text
		"""
		self.canvas.itemconfig(self.T2_text, text='T2 = '+str(data)+'\N{DEGREE SIGN}C')

	def setVoltage(self, data):
		"""
		Set Voltage text
		"""
		self.canvas.itemconfig(self.voltage_text, text=str(round(data,2)) + " mV")

	def setMetal1(self, text):
		"""
		Set metal 1 text
		"""
		self.canvas.itemconfig(self.metal_1_text, text=text)

	def setMetal2(self, text):
		"""
		Set metal 2 text
		"""
		self.canvas.itemconfig(self.metal_2_text, text=text)

"""
Class for creating multi list box. Makes a multicolumn listbox by 
combining a bunch of single listboxes with a single scrollbar. 
I did not create this, I found this on the internet
"""
class MultiListbox(tk.Frame):
	def __init__(self, master=None, columns=2, data=[], row_select=True, **kwargs):
		tk.Frame.__init__(self, master, borderwidth=1, highlightthickness=1, relief=tk.SUNKEN)
		self.rowconfigure(1, weight=1)
		self.columns = columns
		if isinstance(self.columns, (list, tuple)):
			for col, text in enumerate(self.columns):
				tk.Label(self, text=text).grid(row=0, column=col)
			self.columns = len(self.columns)
		self.boxes = []
		for col in range(self.columns):
			box = tk.Listbox(self, exportselection=not row_select, **kwargs)
			if row_select:
				box.bind('<<ListboxSelect>>', self.selected)
			box.grid(row=1, column=col, sticky='nsew')
			self.columnconfigure(col, weight=1)
			self.boxes.append(box)
		vsb = tk.Scrollbar(self, orient=tk.VERTICAL,
			command=multiple(*[box.yview for box in self.boxes]))
		vsb.grid(row=1, column=col+1, sticky='ns')
		for box in self.boxes:
			box.config(yscrollcommand=self.scroll_to_view(vsb.set,
				*[b.yview for b in self.boxes if b is not box]))
		self.add_data(data)
		self.selectRow(0)

	def selectRow(self, row):
		for lbox in self.boxes:
			lbox.select_set(row)

	def selected(self, event=None):
		row = event.widget.curselection()[0]
		for lbox in self.boxes:
			lbox.select_clear(0, tk.END)
			lbox.select_set(row)

	def add_data(self, data=[]):
		boxes = cycle(self.boxes)
		idx = -1
		for idx, (item, box) in enumerate(zip(data, boxes)):
			box.insert(tk.END, item)
		for _ in range(self.columns - idx%self.columns - 1):
			next(boxes).insert(tk.END, '')
		  
	def __getitem__(self, index):
		return [box.get(index) for box in self.boxes]

	def __delitem__(self, index):
		[box.delete(index) for box in self.boxes]

	def curselection(self):
		selection = self.boxes[0].curselection()
		return selection[0] if selection else None

	def scroll_to_view(self, scroll_set, *view_funcs):
		def closure(start, end):
			scroll_set(start, end)
			for func in view_funcs:
				func('moveto', start)
		return closure