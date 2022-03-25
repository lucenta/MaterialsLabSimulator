'''
Description: This file contains the class to create the homepage for the simulation tool
Author: Andrew Lucentini :-)
'''
import tkinter as tk
import Misc.Styling as st
from tkinter import ttk
from PIL import ImageTk, Image
from Misc.helperFunctions import from_rgb
'''
Class to create the main view
'''
class MainView(tk.Frame):
	def __init__(self, parentFrame, controller):
		tk.Frame.__init__(self,parentFrame)

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

		# Create header frame
		header = tk.Frame(mainArea, bg=st.HEADER_BG)
		header.grid(row=0, column=0, rowspan=2, columnspan=20, sticky='nesw')

		# Create title
		label = tk.Label(mainArea, text="Materials science Educational tool: Science emulators", 
			font=st.LARGE_FONT,
			bg = st.HEADER_BG,
			fg = st.INPUT_BG)
		label.grid(row=0, column=0, columnspan=12, rowspan=2, sticky='w')

		# Create description
		label = tk.Label(mainArea, 
			text='Welcome to the Materials Lab Emulator Tool! There are currently 2 emulators '+
				'that you will be using to help futher your understanding of various concepts. ', 
			bg = st.INPUT_BG,
			wraplength=400,
			justify='left',
			relief='groove',
			font=st.MEDIUM_FONT)
		label.grid(row=4, column=6, rowspan=6, columnspan=9, sticky='nesw')
		
		# Create page buttons
		pageNames = ['Mechanical Workshop','Thermocouple Simulator']
		self.pages = []
		for i in range(len(pageNames)):
			b = ttk.Button(mainArea, 
				text=pageNames[i])
			self.pages.append(b)
			b.grid(row=12, column=4+6*i, columnspan=6, rowspan=3, sticky = 'nesw')

		# Disclaimer
		label = tk.Label(mainArea, text="2021, Dr Bosco Yu and Andrew Lucentini, Department of Materials\n" +
										"Science and Engineering & Experiential Learning Office,\nMcMaster University. "+
										"These materials are may be used for educational, research\nand non-commercial purposes only. " +
										"Any other use, including commercial purposes,\nis strictly prohibited. "+
										"If you have questions about your use, please\ncontact Dr Bosco Yu, bosco.yu@mcmaster.ca. "+
										"These materials are provided\non an “as is” basis, without warranty of any kind"+
										" (either express or implied),\nincluding but not limited to any implied warranties "+
										"of merchantability and fitness\nfor a specific or general purpose.",
			font=st.MINI_FONT,
			bg = st.HEADER_BG,
			fg = st.LIGHT_BLUE)
		label.grid(row=0, column=15, columnspan=6, rowspan=5, sticky='nw')

		# Copyright
		label = tk.Label(mainArea, text="Developed by Dr Bosco Yu and Andrew Lucentini\n" +
										"©2022 McMaster University. All rights reserved.", 
			font=st.SMALL_FONT,
			bg = st.MAIN_AREA_BG,
			fg = 'black')
		label.grid(row=19, column=0, columnspan=12, rowspan=2, sticky='w')

		
		# Draw mac logo
		logoImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"macLogo.png"))
		canvas = tk.Canvas(mainArea, bg=st.MAIN_AREA_BG, width=130, height=71, bd=0, highlightthickness=0, relief='ridge')
		canvas.create_image(130/2,71/2, image=logoImg, anchor = "center")
		canvas.image = logoImg
		canvas.grid(row = 17, column = 17, rowspan=3, columnspan=3)