'''
Description: This file contains the class for implementing the thermocouple model.
Author: Andrew Lucentini :-)
'''

"""
Thermocouple model. Used in thermocouple controller
"""
class ThermocoupleModel():
	def __init__(self):
		self.T2 = 25 # T2 temperature in celcius

	def getT2(self):
		"""
		Get T2 temperature
		"""
		return self.T2

	def getData(self):
		"""
		Get seedback coefficients for metals. Each line of the data represents a metal and
		seedback coefficient in the form <metal:seedbackcoef>. This function iterates through 
		each line and returns a list in the form [metal1, seedbackcoef1, metal2, seedbackcoef2..]
		"""
		f = open("Thermocouple/seedbackCoef.txt", 'r')
		data = f.readlines()
		f.close()
		lol = [i.strip("\n").split(":") for i in data]
		result = []
		for i in lol:
			for j in i:
				result.append(j)
		return result

	def calculateVoltage(self, seedback_1, seedback_2, T1):
		"""
		Formula for calculating voltage across thermocouple
		"""
		return -(seedback_1-seedback_2)*(T1-self.T2)