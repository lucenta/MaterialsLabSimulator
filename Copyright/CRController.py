'''
Description: This file contains the classes for implementing the copyright page controller
Author: Andrew Lucentini :-)
'''
from Copyright.CRView import CopyrightView

"""
Copyright page controller
"""
class CopyrightController():
	def __init__(self, parent, mainController):
		self.mainController = mainController

		# Create Views 
		self.page1 = CopyrightView(parent)

		# Bind home
		self.page1.homeButton.bind("<ButtonRelease-1>",self.exitPage)

	def exitPage(self, event):
		"""
		Callback function for exiting the main page. Called when pressing the home button
		"""
		self.mainController.mainPage()