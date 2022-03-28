'''
Description: This file contains the classes for implementing the copyright view
Author: Andrew Lucentini :-)
'''
import tkinter as tk
from tkinter import ttk
from itertools import cycle
import Misc.Styling as st
from PIL import ImageTk, Image

"""
Class for creating the copyright page
"""
class CopyrightView(tk.Frame):
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

		# Create description
		label = tk.Label(mainArea, 
		text="2021, Dr. Bosco Yu and Andrew Lucentini, Department of Materials " +
			"Science and\nEngineering & Experiential Learning Office, McMaster University.\n\n\n"+
			"These materials are may be used for educational, research and\nnon-commercial purposes only. " +
			"Any other use, including commercial\npurposes, is strictly prohibited. "+
			"If you have questions about your use,\nplease contact Dr. Bosco Yu, bosco.yu@mcmaster.ca.\n\n"+
			"These materials are provided on an “as is” basis, without warranty\nof any kind"+
			" (either express or implied), including but\nnot limited to any implied warranties "+
			"of merchantability and fitness\nfor a specific or general purpose.",
			bg = st.INPUT_BG,
			fg = 'black',
			font = st.MEDIUM_FONT,
			justify='center',
			relief='ridge')
		label.grid(row=2, column=1, rowspan=17, columnspan=18, sticky='nesw')
