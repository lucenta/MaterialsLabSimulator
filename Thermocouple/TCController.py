'''
Description: This file contains the classes for implementing the thermocouple page controller!
Author: Andrew Lucentini :-)
'''
from Thermocouple.TCView import ThermocoupleView
from Thermocouple.TCModel import ThermocoupleModel

"""
Thermocouple simulation controller. Utilized in conjuction with the 
thermocouple view and model
"""
class ThermocoupleController():
	def __init__(self, parent, mainController):
		self.mainController = mainController

		# Create Views and model
		self.page1 = ThermocoupleView(parent)
		self.model = ThermocoupleModel()

		# Generate data from model and populate the list boxes
		data = self.model.getData()
		self.page1.populateListboxes(data)
		self.page1.setT2(self.model.getT2())

		# Select first item as default in the list boxes
		for i in range(2):
			self.page1.element_one.boxes[i].select_set(0)
			self.page1.element_two.boxes[i].select_set(0)

		# Set metal 1 and metal 2, calculate initial voltage
		self.metal_1 = self.page1.element_one[0]
		self.metal_2 = self.page1.element_two[0]
		self.calculateVoltage(0)

		# Bind button, slider, and list boxes
		self.page1.homeButton.bind("<ButtonRelease-1>",self.exitPage)
		self.page1.T1.configure(command=self.calculateVoltage)
		for i in range(2):
			self.page1.element_one.boxes[i].bind('<KeyRelease-Down>', self.getElementOne)
			self.page1.element_one.boxes[i].bind('<KeyRelease-Up>', self.getElementOne)
			self.page1.element_one.boxes[i].bind('<ButtonRelease-1>', self.getElementOne)
			self.page1.element_two.boxes[i].bind('<ButtonRelease-1>', self.getElementTwo)
			self.page1.element_two.boxes[i].bind('<KeyRelease-Down>', self.getElementTwo)
			self.page1.element_two.boxes[i].bind('<KeyRelease-Up>', self.getElementTwo)
			
	def calculateVoltage(self, event):
		"""
		Callback function to calculate the voltage across the thermocouple.
		Function is called by moving the T1 slider or by selecting metal one or two
		"""
		temperature = self.page1.T1.get()
		self.page1.setT1(temperature)
		s1 = float(self.metal_1[1])
		s2 = float(self.metal_2[1])
		voltage = self.model.calculateVoltage(s1, s2, temperature)
		self.page1.setVoltage(voltage)
		self.page1.setMetal1(self.metal_1[0])
		self.page1.setMetal2(self.metal_2[0])

	def getElementOne(self, event):
		"""
		Callback function when selecting element one. Triggered by selecting an item from listbox 1
		"""
		index = self.page1.element_one.curselection()
		self.metal_1 = self.page1.element_one[index]
		self.calculateVoltage(0)

	def getElementTwo(self, event):
		"""
		Callback function when selecting element two. Triggered by selecting an item from listbox 2
		"""
		index = self.page1.element_two.curselection()
		self.metal_2 = self.page1.element_two[index]
		self.calculateVoltage(0)

	def exitPage(self, event):
		"""
		Callback function for exiting the main page. Called when pressing the home button
		"""
		self.mainController.mainPage()