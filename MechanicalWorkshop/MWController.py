'''
Description: This file contains the class for the mechanical workshop controller.
Author: Andrew Lucentini :-)
'''
from MechanicalWorkshop.MWModel import TensileTestModel
from MechanicalWorkshop.MWView import TensileTestView, ColdRollerView
import tkinter as tk

"""
Controller for the mechanical workshop simulation
"""
class MechanicalWorkshopController():
	def __init__(self, parent, mainController):
		self.mainController = mainController

		# Create Views and model
		self.page1 = ColdRollerView(parent)
		self.page2 = TensileTestView(parent)
		self.model = TensileTestModel()

		# Page 1 button bindings
		self.page1.disableArrow()
		self.page1.homeButton.bind("<ButtonRelease-1>",self.exitPage)		
		self.page1.animationButton.bind("<Button>", self.cr_AnimationController)
		self.page1.t_0.configure(command = self.calculateColdWork)	
		self.page1.t_f.configure(command = self.calculateColdWork)

		# Page 1 variables
		self.cr_running = False	 	 # Flag for determining if simulation is running
		self.cr_finished = False 	 # Flag for determining if simulation 		
		self.CW = None				 # Percent coldwork. Variable is set by next function call
		self.calculateColdWork(None) # Get initial slider values

		# Page 2 button bindings
		self.page2.animationButton.bind("<Button>", self.tt_AnimationController)
		self.page2.nextPage.bind('<ButtonPress-1>',self.pressArrow)
		self.page2.nextPage.bind('<ButtonRelease-1>',self.releaseArrowPage2)

		# Page 2 variables
		self.tt_running = False	 # Flag for determining if simulation is running
		self.tt_finished = False # Flag for determining if simulation completed			

		self.animationRate = 25  # FPS of animations

	def pressArrow(self, event):
		"""
		Change the arrows if the user presses them
		"""
		self.page1.pressArrow()
		self.page2.pressArrow()

	def releaseArrowPage1(self, event):
		"""
		Change the right arrow when the user releases their click on the right arrow
		"""
		self.page2.normalArrow()
		self.page2.tkraise()

	def releaseArrowPage2(self, event):
		"""
		Change the left arrow when the user releases their click on the left arrow
		"""
		self.resetSimulation()
		self.page1.normalArrow()
		self.page1.tkraise()

	def cr_AnimationController(self, event):
		"""
		Controller for playing and pausing the coldroller animation 
		"""
		if self.cr_running:
			self.cr_running = False
			self.page1.animationButton.config(text='Resume')
		else:
			if self.cr_finished:			
				self.cr_finished = False
			self.cr_running = True
			self.cr_SimulationLoop()
			self.page1.animationButton.config(text='Pause')

			# Make the arrow unclickable if the simulation is playing
			self.page1.disableArrow()
			self.page1.nextPage.unbind('<ButtonPress-1>')
			self.page1.nextPage.unbind('<ButtonRelease-1>')

			# Make the inputs disabled if the simulation is playing
			self.page1.t_0.config(state='disabled')
			self.page1.t_f.config(state='disabled')
			self.page1.t_0.unbind("<B1-Motion>")	
			self.page1.t_f.unbind("<B1-Motion>")

			# Disable the home button
			self.page1.homeButton.config(state='disabled')
			self.page1.homeButton.unbind("<ButtonRelease-1>")

	def tt_AnimationController(self, event):
		""" 
		Controller for playing and pausing the tensile test animation
		"""
		if self.tt_running:
			self.tt_running = False
			self.page2.animationButton.config(text='Resume')

			# Allow the user to leave if they pause the simulation
			self.page2.normalArrow()
			self.page2.nextPage.bind('<ButtonPress-1>',self.pressArrow)
			self.page2.nextPage.bind('<ButtonRelease-1>',self.releaseArrowPage2)
		else:
			if self.tt_finished:
				self.resetSimulation()
				self.tt_finished = False

			# Make the arrow unclickable if the simulation is playing
			self.page2.disableArrow()
			self.page2.nextPage.unbind('<ButtonPress-1>')
			self.page2.nextPage.unbind('<ButtonRelease-1>')

			# Start the simulation again
			self.tt_running = True
			self.tt_SimulationLoop()
			self.page2.animationButton.config(text='Pause')

	def cr_SimulationLoop(self):
		"""
		Simulation loop for performing cold rolling animation
		"""
		if self.cr_running:
			done = self.page1.updateAnimation()	# Update animation
			if done:
				YS, UTS = self.model.setParameters(self.CW) # Set paramaters based on coldwork
				self.page2.setCW(self.CW)					# Send the CW to the tensile test page
				xBounds, yBounds = self.model.init_simVariables(YS, UTS)
				self.page2.setGraphSize(xBounds, yBounds)
				self.cr_running = False
				self.cr_finished = True
				self.page1.animationButton.config(text='Start')
				self.tempCount = 0

				# Make the buttons enabled again
				self.page1.normalArrow()
				self.page1.nextPage.bind('<ButtonPress-1>',self.pressArrow)
				self.page1.nextPage.bind('<ButtonRelease-1>',self.releaseArrowPage1)

				# Make the sliders enabled again
				self.page1.t_0.config(state='normal')
				self.page1.t_f.config(state='normal')
				self.page1.t_0.bind("<B1-Motion>", self.calculateColdWork)	
				self.page1.t_f.bind("<B1-Motion>", self.calculateColdWork)

				# Make the home button enabled again
				self.page1.homeButton.config(state='normal') 	
				self.page1.homeButton.bind("<ButtonRelease-1>",self.exitPage) 	
			else:
				self.page1.after(self.animationRate,self.cr_SimulationLoop) # Call this function again

	def tt_SimulationLoop(self):
		"""
		Simulation loop for performing tensile test animation
		"""
		if self.tt_running:
			xvals, yvals, elongation, guageWidth, neckWidth, neckHeight, done = self.model.updateModel() # Update model
			self.page2.updateAnimation(elongation, guageWidth, neckWidth, neckHeight)				  	 # Update animation
			self.page2.updateGraph(xvals, yvals) 	# Update graph
			if done:
				EL = self.model.getFractureOffset()
				self.page2.generateFracture(EL) 	# Display a 'fracture' based on elongation
				self.tt_running = False
				self.tt_finished = True
				self.page2.animationButton.config(text='Start Over')

				# Make the arrow clickable again
				self.page2.normalArrow()
				self.page2.nextPage.bind('<ButtonPress-1>',self.pressArrow)
				self.page2.nextPage.bind('<ButtonRelease-1>',self.releaseArrowPage2)
			else:
				self.page2.after(self.animationRate,self.tt_SimulationLoop)

	def calculateColdWork(self,event):
		"""
		Calculate the coldwork percentage based on slider values.
		If the slider is modified the next page button is disabled
		until the user runs and finishes the coldwork simulation
		"""
		self.page1.disableArrow()
		self.page1.nextPage.unbind('<ButtonPress-1>')
		self.page1.nextPage.unbind('<ButtonRelease-1>')

		# Get slider values
		t_0 = self.page1.t_0.get()
		t_f = self.page1.t_f.get()
		if t_f > t_0:
			self.page1.t_0.set(t_f)
		if t_0 < t_f:
			self.page1.t_f.set(t_0)

		# Get numbers again because we updated, calculate % coldwork
		t_0 = self.page1.t_0.get()
		t_f = self.page1.t_f.get()

		self.CW = round((t_0-t_f)/t_0*100,2)	# Calculate coldwork
		self.page1.updateCWText(str(self.CW))	# Display coldwork on page
		self.page1.moveRollers(t_f*6, t_0*6, self.CW)	# Move rollers based on t_f and t_0

		# Don't allow user to start if coldwork is greater than 90
		if self.CW > 90:
			self.page1.animationButton.unbind("<Button>")
			self.page1.animationButton.config(state='disabled') 
			self.page1.updateErrorMsg("Warning! Coldwork cannot be greater than 90%")
		else:
			self.page1.animationButton.bind("<Button>", self.cr_AnimationController)
			self.page1.animationButton.config(state='normal') 
			self.page1.updateErrorMsg("")

	def exitPage(self, event):
		"""
		Function to exit page
		"""
		self.resetSimulation()			# Reset Simulation before exiting
		self.mainController.mainPage()	# Raise the mainpage

	def resetSimulation(self):
		"""
		Reset simulation to default
		"""
		self.tt_running = False
		xvals, yvals = self.model.resetData()
		self.page2.updateGraph(xvals,yvals)		# Update graph with data
		self.page2.resetCanvas()				# Reset canvas for drawing rod
		self.page2.animationButton.config(text='Start')