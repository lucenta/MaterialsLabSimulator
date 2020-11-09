'''
Description: This file contains the classes necessary to create the pages for the
			mechanical workshop. In addition, it contains a class to create the cold
			roller animation as well as the rod animation.
Author: Andrew Lucentini :-)
'''
import tkinter as tk
import Misc.Styling as st
import Misc.helperFunctions as hf
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

"""
Class for drawing the cold roller page
"""
class ColdRollerView(tk.Frame):
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
		label = tk.Label(mainArea, text="Mechanical Workshop", 
			font=st.LARGE_FONT,
			bg = st.MAIN_AREA_BG,
			fg = st.TITLE_COLOUR)
		label.grid(row=0, column=14, columnspan=6, sticky='nse')

		# Canvas for graphic simulation
		self.height = 315; self.width = 600
		self.animationWindow = tk.Canvas(mainArea, bg=st.ANIMATION_BG, height=self.height, width=self.width)
		self.animationWindow.grid(row=3, column=0, rowspan=9, columnspan=12, sticky = 'nw')

		# Create cold roller graphic on canvas
		self.coldRoller = ColdRollerGraphic(self.animationWindow, self.width, self.height, st.ANIMATION_BG)
		self.coldRoller.drawRoller()

		# Create description
		label = tk.Label(mainArea, text="Welcome to the mechanical workshop! "+
			"In this emulator you will be studying the effect cold rolling has on "+
			"the material properties of aluminum. Adjust the desired initial (t_0) and "+
			"final (t_f) lengths of the sheet of aluminum that will undergo cold rolling. "+
			"Notice how adjusting the parameters will modify the coldworking percentage. "+
			"Once you have your desired parameters, press start to begin the cold rolling "+
			"process. Do you notice what happens to the grains in the alluminum? "+
			"After the simulation is finished, you can move onto the tensile test "+
			"using the arrow.",
			bg = st.INPUT_BG,
			wraplength=350,
			fg = 'black',
			justify='left',
			relief='ridge')
		label.grid(row=3, column=12, rowspan=6, columnspan=15, sticky='nesw')	

		# Create grid for input area, only used to change colour
		inputArea = tk.Frame(mainArea, bg = st.INPUT_BG, borderwidth=1)
		inputArea.grid(row=12,rowspan=4, column=1, columnspan=10, sticky="nsew")

		# Label and input for t_0
		t0_label = tk.Label(mainArea, text="t_0 (mm): ", 
				bg = st.INPUT_BG,
				fg = 'black')
		self.t_0 = tk.Scale(mainArea, from_=1, to=15, 
			orient=tk.HORIZONTAL, 
			resolution = 0.1, bg=st.INPUT_BG)
		t0_label.grid(row=12, column=0, rowspan=2, columnspan=2, sticky='nsew')
		self.t_0.grid(row=12, column=2, rowspan=2, columnspan=5, sticky='nsew')

		# Label and input for t_f
		tf_label = tk.Label(mainArea, text="t_f (mm): ", 
				bg = st.INPUT_BG,
				fg = 'black')
		self.t_f = tk.Scale(mainArea, from_=1, to=15, 
			orient=tk.HORIZONTAL, 
			resolution = 0.1, bg=st.INPUT_BG)
		tf_label.grid(row=14, column=0, rowspan=2, columnspan=2, sticky='nsew')
		self.t_f.grid(row=14, column=2, rowspan=2, columnspan=5, sticky='nsew')

		# Text for displaying cold work
		self.CW_text = tk.Label(mainArea, text = '', borderwidth=2, bg = st.INPUT_BG)
		self.CW_text.grid(row=14, column=8, rowspan=2, columnspan=2, sticky ='nsew')

		# Button to start simulation
		self.animationButton = ttk.Button(mainArea, text="Start")
		self.animationButton.grid(row=12, column=7, columnspan=4, rowspan=2, sticky='nsew')

		# Buttons to go to next page
		self.arrow = ImageTk.PhotoImage(file = st.IMG_PATH+"right_arrow.png")
		self.arrowClicked = ImageTk.PhotoImage(file = st.IMG_PATH+"right_arrow_clicked.png")
		self.arrowDisabled = ImageTk.PhotoImage(file = st.IMG_PATH+"right_arrow_disabled.png")

		# Draw initial button
		self.nextPage = tk.Button(mainArea, image=self.arrow, borderwidth=0)
		self.nextPage.image = self.arrowDisabled
		self.nextPage.grid(row=10, rowspan=2, column=19, sticky = 'nesw')

		# Create error message
		self.errMsg = tk.Label(mainArea, text='', borderwidth=0, bg=st.MAIN_AREA_BG, fg='red')
		self.errMsg.grid(row = 16, column = 1, columnspan=10)

		# Draw mac logo
		logoImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"macLogo.png"))
		canvas = tk.Canvas(mainArea, bg=st.MAIN_AREA_BG, width=130, height=71, bd=0, highlightthickness=0, relief='ridge')
		canvas.create_image(130/2,71/2, image=logoImg, anchor = "center")
		canvas.image = logoImg
		canvas.grid(row = 17, column = 17, rowspan=3, columnspan=3)

	def pressArrow(self):
		"""
		Change arrow picture to "pressed arrow"
		"""
		self.nextPage.config(image = self.arrowClicked)
		self.nextPage.image = self.arrowClicked

	def normalArrow(self):
		"""
		Change arrow picture to "normal arrow"
		"""
		self.nextPage.config(image = self.arrow)
		self.nextPage.image = self.arrow

	def disableArrow(self): 
		"""
		Change arrow picture to "disabled arrow"
		"""
		self.nextPage.config(image = self.arrowDisabled)
		self.nextPage.image = self.arrowDisabled

	def updateCWText(self, val):
		"""
		Change coldwork text to val
		"""
		self.CW_text.config(text="%CW = "+val)

	def moveRollers(self, t_f, t_0, CW):
		"""
		Move the rollers in the cold coller
		"""
		self.coldRoller.updateRollers(t_f,t_0, CW)

	def updateAnimation(self):
		done = self.coldRoller.updateAni()
		return done

	def updateErrorMsg(self, errText):
		"""
		Update error message
		"""
		self.errMsg.config(text=errText)

"""
Class for drawing the tensile test page
"""
class TensileTestView(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent) # Initialize this class as a frame
		self.animationBgCol = "black"	# Animation canvas background colour

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

		# Create title
		label = tk.Label(mainArea, text="Mechanical Workshop", 
			font=st.LARGE_FONT,
			bg = st.MAIN_AREA_BG,
			fg = st.TITLE_COLOUR)
		label.grid(row=0, column=14, columnspan=6, sticky='nse')

		# Create description
		label = tk.Label(mainArea, text="We are now going to perform a tensile test on the "+
			"sheet of aluminum that we cold rolled! We can see our sample of aluminum on the left side of "+
			"the screen as well as a stress-strain graph on the right side of the screen. "+
			"Press the start button to begin the tensile test!",
			bg = st.INPUT_BG,
			wraplength=650,
			fg = 'black',
			justify='left',
			relief='ridge')
		label.grid(row=1, column=6, rowspan=2, columnspan=14, sticky='nesw')	

		# Canvas for graphic simulation
		self.height = 595; self.width = 250
		self.animationWindow = tk.Canvas(mainArea, 
			bg=self.animationBgCol, height=self.height, width=self.width,
			bd=0, highlightthickness=0, relief='ridge')
		self.animationWindow.grid(row=2, column=1, columnspan=5, rowspan=17, sticky='ne')

		# Create Plot
		self.f = Figure(figsize=(6,6), dpi=100)
		self.a = self.f.add_subplot(111)
		self.a.grid(color='grey', linestyle='-', linewidth=0.3)
		self.a.set_ylabel('Stress (MPa)')
		self.a.set_xlabel('Strain (-)')
		self.line = self.a.plot([],[],"-")
		self.a.format_coord = lambda x, y: "Strain (-)={:6.4f}, Stress (MPa)={:6.3f}".format(x,y)

		# Create canvas for plot
		self.graphWindow = FigureCanvasTkAgg(self.f, mainArea)
		self.graphWindow.get_tk_widget().grid(row=5,column=6, rowspan=12, columnspan=12)		
		self.BG = self.graphWindow.copy_from_bbox(self.a.bbox)
		self.OG = self.BG

		# Load arrow images
		self.arrow = ImageTk.PhotoImage(file = st.IMG_PATH+"left_arrow.png")
		self.arrowClicked = ImageTk.PhotoImage(file = st.IMG_PATH+"left_arrow_clicked.png")
		self.arrowDisabled = ImageTk.PhotoImage(file = st.IMG_PATH+"left_arrow_disabled.png")

		# Arrow for previous page
		self.nextPage = tk.Button(mainArea, image=self.arrow, borderwidth=0)
		self.nextPage.image = self.arrow
		self.nextPage.grid(row=9, rowspan=2, column=0, sticky = 'nesw')

		# Button to start simulation
		self.animationButton = ttk.Button(mainArea, text="Start")
		self.animationButton.grid(row=3, rowspan=2, column=6, columnspan=3, sticky = 'nesw')

		# Text for displaying cold work
		self.CW_text = tk.Label(mainArea, text = '', borderwidth=2, bg = st.INPUT_BG, font=st.MEDIUM_FONT)
		self.CW_text.grid(row=0, rowspan=2, column=2, columnspan=3, sticky ='nsew')

		# Draw the rod
		self.rod = Rod(self.animationWindow, self.width, self.height, self.animationBgCol)
		self.rod.drawRod()

		# Create toolbar for plot
		self.toolbar = NavigationToolbar2Tk(self.graphWindow, mainArea)
		self.toolbar.update()
		self.toolbar.grid(row = 17, column = 6, rowspan=2, columnspan=10, sticky='nsew')

		# Draw mac logo
		logoImg = ImageTk.PhotoImage(Image.open(st.IMG_PATH+"macLogo.png"))
		canvas = tk.Canvas(mainArea, bg=st.MAIN_AREA_BG, width=130, height=71, bd=0, highlightthickness=0, relief='ridge')
		canvas.create_image(130/2,71/2, image=logoImg, anchor = "center")
		canvas.image = logoImg
		canvas.grid(row = 17, column = 17, rowspan=3, columnspan=3)

	def setGraphSize(self, x, y):
		"""
		Set the graph size. Assume it is called before any other function
		"""
		self.a.set_xlim([-0.01, x+0.3])
		self.a.set_ylim([0, y+50])
		self.graphWindow.draw()
		self.BG = self.graphWindow.copy_from_bbox(self.a.bbox)

	def pressArrow(self):
		"""
		Change arrow picture to "pressed arrow"
		"""
		self.nextPage.config(image = self.arrowClicked)
		self.nextPage.image = self.arrowClicked

	def normalArrow(self):
		"""
		Change arrow picture to "normal arrow"
		"""
		self.nextPage.config(image = self.arrow)
		self.nextPage.image = self.arrow

	def disableArrow(self):
		"""
		Change arrow picture to "disabled arrow"
		"""
		self.nextPage.config(image = self.arrowDisabled)
		self.nextPage.image = self.arrowDisabled

	def resetCanvas(self):
		"""
		Reset the rod on canvas
		"""
		self.rod.resetRod()

	def setCW(self, val):
		"""
		Set the coldwork text
		"""
		self.CW_text.config(text="%CW = "+str(val))

	def updateGraph(self, xvals, yvals):
		"""
		Update the graph with xvals and yvals. This function is called at a given framerate
		"""
		self.line[0].set_data(xvals,yvals)
		self.graphWindow.restore_region(self.BG)
		self.a.draw_artist(self.line[0])
		self.graphWindow.blit(self.a.bbox)
		self.graphWindow.flush_events()

	def updateAnimation(self, elongation, widthFact, neckWidthFact, neckHeightFact):
		"""
		Update the canvas based on given values. This function is called at a given framerate
		"""
		self.rod.updateRod(elongation, widthFact, neckWidthFact, neckHeightFact)

	def generateFracture(self, EL):
		"""
		Generate a fracture in the Rod. Function is called at the end of the animation
		"""
		self.rod.drawFracture(EL)

"""
Class for drawing the cold roller graphic
"""
class ColdRollerGraphic():
	def __init__(self, canvas, canvasWidth, canvasHeight, bg):
		self.bg = bg
		self.canvas = canvas
		self.height = canvasHeight
		self.width = canvasWidth

		# Initialize roller images
		self.t_rollermask = Image.open(st.IMG_PATH+"rollerTop.png")
		self.b_rollermask = Image.open(st.IMG_PATH+"rollerBottom.png") 
		self.img_mask = Image.open(st.IMG_PATH+"CW_75_to_90.png")
		# self.height = 315; self.width = 600
		self.t_rollerimg = ImageTk.PhotoImage(self.t_rollermask.rotate(0))
		self.b_rollerimg = ImageTk.PhotoImage(self.b_rollermask.rotate(0))
		self.background_img = ImageTk.PhotoImage(self.img_mask)
		self.roller_radius = self.t_rollermask.size[0]/2

		# Top roller coordinates. Coordinates are center of image
		self.tr_x = self.width/2
		self.tr_y = self.height/2-self.roller_radius

		# Bottom roller coordinates. Coordinates are center of image
		self.br_x = self.width/2
		self.br_y = self.height/2+self.roller_radius

		# Use 'blocks' to hide portions of the metal to simulate "rolling" through the rollers
		# Right block coordinates
		self.x0_rb = self.width/2-self.roller_radius
		self.y0_rb = 0
		self.x1_rb = self.width+5
		self.y1_rb = self.height+5

		# Top right block coordinates
		self.x0_trb = self.width/2-self.roller_radius
		self.y0_trb = 0
		self.x1_trb = self.width+5
		self.y1_trb = self.height/2

		# Bottom right block coordinates
		self.x0_brb = self.width/2-self.roller_radius
		self.y0_brb = self.height/2
		self.x1_brb = self.width+5
		self.y1_brb = self.height+5

		# Top left block coordinates
		self.x0_tlb = 0
		self.y0_tlb = 0
		self.x1_tlb = self.width/2
		self.y1_tlb = self.height/2

		# Bottom left block coordinates
		self.x0_blb = 0
		self.y0_blb = self.height/2
		self.x1_blb = self.width/2
		self.y1_blb = self.height

		# Bottom left block coordinates
		self.x0_lb = 0
		self.y0_lb = 0
		self.x1_lb = self.width/20
		self.y1_lb = self.height

		# Variables used in simulation to manage roller and sheet movement
		self.rollerCount = 0
		self.sheetCount = 0
		self.sheetInc = 4
		self.rollerInc = 10

		# Keep track of t_f and t_0
		self.t_f = 0
		self.t_0 = 0

	def drawRoller(self):
		"""
		Draw the roller
		"""
		self.backGround = self.canvas.create_image(0,0, image = self.background_img, anchor = 'nw')

		# Draw rectangles to cover up background
		self.rightBlock = self.canvas.create_rectangle(
			self.x0_rb, self.y0_rb, 
			self.x1_rb, self.y1_rb, 
			fill = self.bg, outline = '')

		self.topRightBlock = self.canvas.create_rectangle(
			self.x0_trb, self.y0_trb, 
			self.x1_trb, self.y1_trb,
			fill = self.bg, outline = '')

		self.bottomRightBlock = self.canvas.create_rectangle(
			self.x0_brb, self.y0_brb, 
			self.x1_brb, self.y1_brb,
			fill = self.bg, outline = '')

		self.topLeftBlock = self.canvas.create_rectangle(
			self.x0_tlb, self.y0_tlb,
			self.x1_tlb, self.y1_tlb,
			fill = self.bg, outline = '')

		self.bottomLeftBlock = self.canvas.create_rectangle(
			self.x0_blb, self.y0_blb,
			self.x1_blb, self.y1_blb,
			fill = self.bg, outline = '')

		self.leftBlock = self.canvas.create_rectangle(
			self.x0_lb, self.y0_lb,
			self.x1_lb, self.y1_lb,
			fill = self.bg, outline = '')

		# Draw lines to outline visible area
		self.leftVertical = self.canvas.create_line(
			self.x1_lb,self.y1_tlb,
			self.x1_lb,self.y0_blb,
			fill='black', width = 2)

		self.topLeftHorizontal = self.canvas.create_line(
			self.x1_lb,self.y1_tlb,
			self.x0_trb,self.y1_tlb,
			fill='black', width = 2)

		self.bottomLeftHorizontal = self.canvas.create_line(
			self.x1_lb,self.y0_blb,
			self.x0_brb,self.y0_blb,
			fill='black', width = 2)

		# Don't care about the initial right lines
		self.farRightVertical = self.canvas.create_line(
			0,0,0,0,
			fill='black', width = 2)

		self.rightVertical = self.canvas.create_line(
			0,0,0,0,
			fill='black', width = 2)

		self.topRightHorizontal = self.canvas.create_line(
			0,0,0,0,
			fill='black', width = 2)

		self.bottomRightHorizontal = self.canvas.create_line(
			0,0,0,0,
			fill='black', width = 2)

		self.topRoller = self.canvas.create_image(self.tr_x,self.tr_y, image = self.t_rollerimg, anchor = tk.CENTER)
		self.bottomRoller = self.canvas.create_image(self.br_x, self.br_y, image = self.b_rollerimg, anchor = tk.CENTER)

	def updateRollers(self, t_f, t_0, CW):
		"""
		Update the roller position based on t_f and t_0
		"""
		self.t_f = t_f
		self.t_0 = t_0

		# Change background based on CW percent
		newImg=""
		if CW <= 15:
			newImg ="CW_0_to_15.png"
		elif CW <= 30:
			newImg ="CW_15_to_30.png"
		elif CW <= 75:
			newImg ="CW_30_to_75.png"
		else:
			newImg ="CW_75_to_90.png"
		self.canvas.delete(self.backGround)
		self.background_img = ImageTk.PhotoImage(Image.open(st.IMG_PATH+newImg))
		self.backGround = self.canvas.create_image(0,0, image = self.background_img, anchor = 'nw')
		self.canvas.tag_lower(self.backGround)

		# Update roller positions
		self.canvas.coords(self.topRoller, self.tr_x, self.tr_y-t_f)
		self.canvas.coords(self.bottomRoller, self.br_x, self.br_y+t_f)

		# Update block positions
		self.canvas.coords(self.topRightBlock, self.x0_trb, self.y0_trb-t_f, self.x1_trb, self.y1_trb-t_f)
		self.canvas.coords(self.bottomRightBlock, self.x0_brb, self.y0_brb+t_f, self.x1_brb, self.y1_brb+t_f)
		self.canvas.coords(self.topLeftBlock, self.x0_tlb, self.y0_tlb-t_0, self.x1_tlb, self.y1_tlb-t_0)
		self.canvas.coords(self.bottomLeftBlock, self.x0_blb, self.y0_blb+t_0, self.x1_blb, self.y1_blb+t_0)
		self.canvas.coords(self.rightBlock, self.x0_rb, self.y0_rb, self.x1_rb, self.y1_rb)
		self.canvas.coords(self.leftBlock, self.x0_lb, self.y0_lb, self.x1_lb, self.y1_lb)

		# Update line positions
		self.canvas.coords(self.leftVertical, self.x1_lb, self.y1_tlb-t_0, self.x1_lb, self.y0_blb+t_0)
		self.canvas.coords(self.topLeftHorizontal, self.x1_lb, self.y1_tlb-t_0, self.x0_trb, self.y1_tlb-t_0)
		self.canvas.coords(self.bottomLeftHorizontal, self.x1_lb, self.y0_blb+t_0, self.x0_brb, self.y0_blb+t_0)
		self.canvas.coords(self.farRightVertical, self.x0_rb, self.y1_tlb-t_0, self.x0_rb, self.y0_blb+t_0)

		# Make the necessary right lines hidden
		for i in (self.rightVertical, self.topRightHorizontal, self.bottomRightHorizontal):
			self.canvas.coords(i, self.width/2, self.height/2, self.width/2, self.height/2)

	def updateAni(self):
		"""
		Update the cold roller animation. This function is called at an interval
		"""
		self.rollerCount += self.rollerInc
		self.sheetCount += self.sheetInc
		x,y = self.canvas.coords(self.topRoller)
		x1,y1 = self.canvas.coords(self.bottomRoller)

		# Update the roller image by rotating it
		self.canvas.delete(self.t_rollerimg)
		self.canvas.delete(self.b_rollerimg)
		self.t_rollerimg = ImageTk.PhotoImage(self.t_rollermask.rotate(self.rollerCount))
		self.b_rollerimg = ImageTk.PhotoImage(self.b_rollermask.rotate(-self.rollerCount))
		self.topRoller = self.canvas.create_image(x,y, image = self.t_rollerimg, anchor = tk.CENTER)
		self.bottomRoller = self.canvas.create_image(x1,y1, image = self.b_rollerimg, anchor = tk.CENTER)

		#  Move the blocks and lines a certain way if the right side hasn't gotten to the center of the rollers
		r_amount = self.x0_rb+self.sheetCount
		r_left_amount = self.x1_lb+self.sheetCount
		if r_amount <= self.width/2:
			self.canvas.coords(self.topRightBlock, self.x0_trb+self.sheetCount, self.y0_trb-self.t_f, self.x1_trb, self.y1_trb-self.t_f)
			self.canvas.coords(self.bottomRightBlock, self.x0_brb+self.sheetCount, self.y0_brb+self.t_f, self.x1_brb, self.y1_brb+self.t_f)
			self.canvas.coords(self.topLeftHorizontal, self.x1_lb+self.sheetCount, self.y1_tlb-self.t_0, self.x0_trb+self.sheetCount, self.y1_tlb-self.t_0)
			self.canvas.coords(self.bottomLeftHorizontal, self.x1_lb+self.sheetCount, self.y0_blb+self.t_0, self.x0_brb+self.sheetCount, self.y0_blb+self.t_0)
			self.canvas.coords(self.leftVertical, self.x1_lb+self.sheetCount, self.y1_tlb-self.t_0, self.x1_lb+self.sheetCount, self.y0_blb+self.t_0)
			self.canvas.coords(self.farRightVertical, r_amount, self.y1_tlb-self.t_0, r_amount, self.y0_blb+self.t_0)
		else: 
			# Move the blocks and lines a different way if the left side passed the center of the rollers
			if r_left_amount >= self.width/2:
				self.canvas.coords(self.topLeftHorizontal, self.width/2, self.y1_tlb-self.t_0, self.width/2, self.y1_tlb-self.t_0)
				self.canvas.coords(self.bottomLeftHorizontal, self.width/2, self.y0_blb+self.t_0, self.width/2, self.y0_blb+self.t_0)
				self.canvas.coords(self.leftVertical, self.width/2, self.y0_blb+self.t_0, self.width/2, self.y0_blb+self.t_0)
				self.canvas.coords(self.rightVertical, r_left_amount, self.y1_trb-self.t_f, r_left_amount, self.y0_brb+self.t_f)
				self.canvas.coords(self.topRightHorizontal, r_left_amount, self.y1_trb-self.t_f, r_amount, self.y1_trb-self.t_f)
				self.canvas.coords(self.bottomRightHorizontal, r_left_amount, self.y0_brb+self.t_f, r_amount, self.y0_brb+self.t_f)
			# Move yet a diff way if the left side haven't passed the center
			else:
				self.canvas.coords(self.topLeftHorizontal, self.x1_lb+self.sheetCount, self.y1_tlb-self.t_0, self.width/2, self.y1_tlb-self.t_0)
				self.canvas.coords(self.bottomLeftHorizontal, self.x1_lb+self.sheetCount, self.y0_blb+self.t_0, self.width/2, self.y0_blb+self.t_0)
				self.canvas.coords(self.leftVertical, self.x1_lb+self.sheetCount, self.y1_tlb-self.t_0, self.x1_lb+self.sheetCount, self.y0_blb+self.t_0)
				self.canvas.coords(self.topRightHorizontal, self.width/2, self.y1_trb-self.t_f, r_amount, self.y1_trb-self.t_f)
				self.canvas.coords(self.bottomRightHorizontal, self.width/2, self.y0_brb+self.t_f, r_amount, self.y0_brb+self.t_f)
			self.canvas.coords(self.farRightVertical, r_amount, self.y1_trb-self.t_f, r_amount, self.y0_brb+self.t_f)

		# Always move left and right blocks
		self.canvas.coords(self.rightBlock, self.x0_rb+self.sheetCount, self.y0_rb, self.x1_rb, self.y1_rb)
		self.canvas.coords(self.leftBlock, self.x0_lb, self.y0_lb, self.x1_lb+self.sheetCount, self.y1_lb)

		# Updating bounding lines
		# self.canvas.coords(self.leftVertical, self.x1_lb, self.y1_tlb-t_0, self.x1_lb, self.y0_blb+t_0)

		# Stop the simulation when we reach 2 rotations
		if self.rollerCount == 720:
			self.rollerCount = 0
			self.sheetCount = 0
			self.count3 = 0
			done = True
		else:
			done = False
		return done

"""
Class for drawing the tensile rod
"""
class Rod():
	def __init__(self, canvas, canvasWidth, canvasHeight, canvasBGcolour):

		self.animationBgCol = canvasBGcolour
		self.canvas = canvas
		self.height = canvasHeight
		self.width = canvasWidth
		self.gripperColour = 'orange'
		self.guageColour = 'grey'

		# Guage area dimentions
		self.guageWidth = 60
		self.guageLength = 250

		# Rounded part of rod that makes "dogbone" shape
		self.roundedLength = 30
		self.roundedWidth = 20

		# Gripper dimensions
		self.gripWidth = 100
		self.gripLength = 60

		# Guage area coordinates
		self.guage = None
		self.g_x0 = self.width/2-self.guageWidth/2
		self.g_y0 = self.height/2-self.guageLength/2
		self.g_x1 = self.width/2+self.guageWidth/2
		self.g_y1 = self.height/2+self.guageLength/2

		# Left Neck coordinates
		self.leftNeck = None
		self.ln_x0 = self.width/2-self.guageWidth/2-1
		self.ln_y0 = self.height/2
		self.ln_x1 = self.width/2-self.guageWidth/2-1
		self.ln_y1 = self.height/2

		# Right Neck coordinates
		self.rightNeck = None
		self.rn_x0 = self.width/2+self.guageWidth/2
		self.rn_y0 = self.height/2
		self.rn_x1 = self.width/2+self.guageWidth/2
		self.rn_y1 = self.height/2

		# Top Blank area
		self.topBlank = None
		self.tb_x0 = self.width/2-self.guageWidth/2-self.roundedWidth
		self.tb_y0 = self.height/2-self.guageLength/2-self.roundedLength
		self.tb_x1 = self.width/2+self.guageWidth/2+self.roundedWidth
		self.tb_y1 = self.height/2-self.guageLength/2

		# Top left fillet
		self.topLeftFillet = None
		self.tlf_x0 = self.width/2-self.guageWidth/2-2*self.roundedWidth-1
		self.tlf_y0 = self.height/2-self.guageLength/2-self.roundedLength
		self.tlf_x1 = self.width/2-self.guageWidth/2-1
		self.tlf_y1 = self.height/2-self.guageLength/2+self.roundedLength

		# Top right fillet
		self.topRightFillet = None
		self.trf_x0 = self.width/2+self.guageWidth/2
		self.trf_y0 = self.height/2-self.guageLength/2-self.roundedLength
		self.trf_x1 = self.width/2+self.guageWidth/2+2*self.roundedWidth
		self.trf_y1 = self.height/2-self.guageLength/2+self.roundedLength

		# Bottom Blank area
		self.bottomBlank = None
		self.bb_x0 = self.width/2-self.guageWidth/2-self.roundedWidth
		self.bb_y0 = self.height/2+self.guageLength/2
		self.bb_x1 = self.width/2+self.guageWidth/2+self.roundedWidth
		self.bb_y1 = self.height/2+self.guageLength/2+self.roundedLength

		# Bottom left fillet
		self.bottomLeftFillet = None
		self.blf_x0 = self.width/2-self.guageWidth/2-2*self.roundedWidth-1
		self.blf_y0 = self.height/2+self.guageLength/2-self.roundedLength
		self.blf_x1 = self.width/2-self.guageWidth/2-1
		self.blf_y1 = self.height/2+self.guageLength/2+self.roundedLength

		# Bottom right fillet
		self.bottomRightFillet = None
		self.brf_x0 = self.width/2+self.guageWidth/2
		self.brf_y0 = self.height/2+self.guageLength/2-self.roundedLength
		self.brf_x1 = self.width/2+self.guageWidth/2+2*self.roundedWidth
		self.brf_y1 = self.height/2+self.guageLength/2+self.roundedLength

		# Top gripper coordinates
		self.topGrip = None
		self.tg_x0 = self.width/2-self.gripWidth/2
		self.tg_y0 = self.height/2-self.guageLength/2-self.gripLength-self.roundedLength
		self.tg_x1 = self.width/2+self.gripWidth/2
		self.tg_y1 = self.height/2-self.guageLength/2-self.roundedLength

		# Bottom gripper coordinates
		self.bottomGrip = None
		self.bg_x0 = self.width/2-self.gripWidth/2
		self.bg_y0 = self.height/2+self.guageLength/2+self.roundedLength
		self.bg_x1 = self.width/2+self.gripWidth/2
		self.bg_y1 = self.height/2+self.guageLength/2+self.gripLength+self.roundedLength

	def drawRod(self):
		"""
		Draw the rod
		"""
		# Draw guage area 
		self.guage = self.canvas.create_rectangle(
			self.g_x0, self.g_y0, 
			self.g_x1, self.g_y1, 
			fill = self.guageColour, outline = '')

		# Draw left neck
		self.leftNeck = self.canvas.create_oval(
			self.ln_x0, self.ln_y0, 
			self.ln_x1, self.ln_y1,
			fill = self.animationBgCol, outline = '')

		# Draw right neck
		self.rightNeck = self.canvas.create_oval(
			self.rn_x0, self.rn_y0, 
			self.rn_x1, self.rn_y1,
			fill = self.animationBgCol, outline = '')

		# Draw top blank area
		self.topBlank = self.canvas.create_rectangle(
			self.tb_x0, self.tb_y0,
			self.tb_x1, self.tb_y1,
			fill = self.guageColour, outline = '')

		# Draw top left fillet
		self.topLeftFillet = self.canvas.create_oval(
			self.tlf_x0, self.tlf_y0,
			self.tlf_x1, self.tlf_y1,
			outline='', fill = self.animationBgCol)

		# Draw top right fillet
		self.topRightFillet = self.canvas.create_oval(
			self.trf_x0, self.trf_y0,
			self.trf_x1, self.trf_y1,
			outline='', fill = self.animationBgCol)

		# Draw bottom blank area
		self.bottomBlank = self.canvas.create_rectangle(
			self.bb_x0, self.bb_y0,
			self.bb_x1, self.bb_y1,
			fill = self.guageColour, outline = '')

		# Draw bottom left fillet
		self.bottomLeftFillet = self.canvas.create_oval(
			self.blf_x0, self.blf_y0,
			self.blf_x1, self.blf_y1,
			outline='', fill = self.animationBgCol)

		# Draw bottom right fillet
		self.bottomRightFillet = self.canvas.create_oval(
			self.brf_x0, self.brf_y0,
			self.brf_x1, self.brf_y1,
			outline='', fill = self.animationBgCol)

		# Draw top gripper
		self.topGrip = self.canvas.create_rectangle(
			self.tg_x0, self.tg_y0, 
			self.tg_x1, self.tg_y1, 
			fill = self.gripperColour, outline = '')

		# Draw bottom gripper
		self.bottomGrip = self.canvas.create_rectangle(
			self.bg_x0, self.bg_y0,
			self.bg_x1, self.bg_y1,
			fill = self.gripperColour, outline = '')

	def updateRod(self, elongation, widthFact, neckWidthFact, neckHeightFact):
		"""
		Update the rod position based on initial drawing. Must be called after drawRod
		"""
		e = elongation*50								# Scale longation pixels
		eFact = (self.guageLength+2*e)/self.guageLength	# Convert longation to percentange
		
		# Redraw Guage
		x,y,x1,y1 = hf.scaleCoordinates(self.g_x0, self.g_y0, self.g_x1, self.g_y1, widthFact, eFact)
		self.canvas.coords(self.guage, x, y, x1, y1)
		leftPos = x
		rightPos = x1

		# Redraw left neck
		dx = neckWidthFact*(self.guageWidth)
		dy = neckHeightFact*(self.guageWidth)
		x,y,x1,y1 = hf.translateCoordinates(self.ln_x0, self.ln_y0, self.ln_x1 ,self.ln_y1, leftPos-self.ln_x0, 0)
		x,y,x1,y1 = hf.stretchCoordinates(x-1,y,x1-1,y1,dx,dy)
		self.canvas.coords(self.leftNeck, x, y, x1, y1)

		# Redraw right neck
		x,y,x1,y1 = hf.translateCoordinates(self.rn_x0, self.rn_y0, self.rn_x1 ,self.rn_y1,-(self.rn_x1-rightPos), 0)
		x,y,x1,y1 = hf.stretchCoordinates(x,y,x1,y1,dx,dy)
		self.canvas.coords(self.rightNeck, x, y, x1, y1)

		# Redraw top left fillet
		x,y,x1,y1 = hf.translateCoordinates(self.tlf_x0, self.tlf_y0, self.tlf_x1, self.tlf_y1, 0, -e)
		self.canvas.coords(self.topLeftFillet,x,y,leftPos-1,y1)

		# Redraw top right fillet
		x,y,x1,y1 = hf.translateCoordinates(self.trf_x0, self.trf_y0, self.trf_x1, self.trf_y1, 0, -e)
		self.canvas.coords(self.topRightFillet,rightPos,y,x1,y1)

		# Redraw bottom left fillet
		x,y,x1,y1 = hf.translateCoordinates(self.blf_x0, self.blf_y0, self.blf_x1, self.blf_y1, 0, e)
		self.canvas.coords(self.bottomLeftFillet,x,y,leftPos-1,y1)

		# Redraw bottom right fillet
		x,y,x1,y1 = hf.translateCoordinates(self.brf_x0, self.brf_y0, self.brf_x1, self.brf_y1, 0, e)
		self.canvas.coords(self.bottomRightFillet,rightPos,y,x1,y1)

		# Redraw top blank area
		x,y,x1,y1 = hf.translateCoordinates(self.tb_x0, self.tb_y0, self.tb_x1, self.tb_y1, 0, -e)
		self.canvas.coords(self.topBlank,x,y,x1,y1)

		# Redraw bottom blank area
		x,y,x1,y1 = hf.translateCoordinates(self.bb_x0, self.bb_y0, self.bb_x1, self.bb_y1, 0, e)
		self.canvas.coords(self.bottomBlank,x,y,x1,y1)

		# Redraw top gripper
		x,y,x1,y1 = hf.translateCoordinates(self.tg_x0, self.tg_y0, self.tg_x1, self.tg_y1, 0, -e)
		self.canvas.coords(self.topGrip, x, y, x1, y1)

		# Redraw bottom gripper
		x,y,x1,y1 = hf.translateCoordinates(self.bg_x0, self.bg_y0, self.bg_x1 ,self.bg_y1, 0, e)
		self.canvas.coords(self.bottomGrip, x, y, x1, y1)

	def drawFracture(self, curvature):
		"""
		Emulate a fracture. Called at the end of the simulation
		"""
		# Draw an arc with a curvature
		self.canvas.create_arc(
			self.width/2-self.guageWidth/2, self.height/2-curvature*300,
			self.width/2+self.guageWidth/2, self.height/2,
			start = 180, extent = 180 , width=5, style=tk.ARC)

	def resetRod(self):
		"""
		Reset the rod to the original
		"""
		self.canvas.delete("all")
		self.drawRod()