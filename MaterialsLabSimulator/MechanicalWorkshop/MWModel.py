'''
Description: This file contains the model for the tensile test
Author: Andrew Lucentini :-)
		Dr. Zurob Hatem (zurobh@mcmaster.ca)
		Dr. Bosco Yu (bosco.yu@mcmaster.ca)
'''
import random
from math import exp, log

"""
Model for the tensile test. This class contains the state of a tesnsile test
at a given position in "time". The tensile test is split into 3 regions:
The elastic region, the strain hardening, and then the necking region. The math
for each region can be seen in the updateModel function
"""
class TensileTestModel():
	def __init__(self):
		# Inputs are set in the init_simVariables function
		self.E = 69000 # E constant in MPa
		self.UTS = None # UTS constant in MPa
		self.YS = None # Yield strength in MPa
		self.EL = None # strain constant, unitless

		# Data for simulation
		self.Xvals = []
		self.Yvals = []

		# Material parameters based on aluminum
		self.YS_0 = 60
		self.YS_INF = 220
		self.CW_C = 45
		self.UTS_0 = 110
		self.UTS_INF = 223
		self.M_EL = 0.0045
		self.C_EL = 0.01
	
	def setParameters(self, CW):
		"""
		Modify parameters based on coldwork
		"""
		self.YS = self.YS_INF-(self.YS_INF-self.YS_0)*exp(-CW/self.CW_C)
		self.UTS = self.UTS_INF-(self.UTS_INF-self.UTS_0)*exp(-CW/self.CW_C)
		self.EL = 1/(self.M_EL*CW+self.C_EL)
		self.EL = self.EL/100
		return self.YS, self.UTS

	def init_simVariables(self, YS, UTS):
		"""
		Initialize the simulation variables
		"""
		# Change number of points based on YS and UTS to make simulation run more smoothly
		ratio = UTS/YS
		if ratio > 1.5:
			self.s1Points = 20		# Number of data points in stage 1
			self.s2_s3Points = 100  # Number of data points in stage 2 and stage 3
		elif ratio > 1.3:
			self.s1Points = 40
			self.s2_s3Points = 80
		else:
			self.s1Points = 60
			self.s2_s3Points = 40 

		# Stage 1 variables
		self.s1CurPoint = 0
		self.s1Inc = 1/self.s1Points # How much to incrememnt each point

		# Stage 2 and 3 variables
		self.s2_s3CurPoint = 0
		self.s2_s3Inc = 1/self.s2_s3Points 			  # How much to increment each point
		self.neckingPoint = int(self.s2_s3Points*.60) # Point to transition from stage 2 to stage 3

		# Constants
		self.ELmult = 1.2*self.EL
		self.ELfact = self.EL/6
		self.UTS_YS_diff = self.UTS-self.YS

		return self.EL, self.UTS

	def resetData(self):
		"""
		Resets the Simulation to default
		"""
		self.Xvals = []
		self.Yvals = []
		self.s1CurPoint = 0
		self.s2_s3CurPoint = 0
		return self.Xvals, self.Yvals

	def getFractureOffset(self):
		"""
		Use the self.EL constant to determine fracture curvature.
		The greater the self.EL the greater the curvature.
		"""
		return self.EL

	def updateModel(self):
		"""
		Function to update the state of the model. 
		This function is called at a specific interval
		"""
		done = False
		# Stage 1 of curve
		if self.s1CurPoint < self.s1Points:
			stress = self.YS*self.s1CurPoint*self.s1Inc # Engineering Stress
			stress_true = stress # True Stress
			total_strain = stress/self.E
			self.s1CurPoint += 1
			w = exp(-log(1+total_strain)) 		# Relative guage uniform width
			n = w
		# Stage 2 of curve
		elif self.s2_s3CurPoint <= self.neckingPoint:
			pl_strain = self.EL*self.s2_s3CurPoint*self.s2_s3Inc
			stress = self.UTS-self.UTS_YS_diff*exp(-pl_strain/self.ELfact) # Engineering Stress
			stress_true = stress # True Stress
			tot_strain = stress/self.E
			total_strain = tot_strain+pl_strain
			self.s2_s3CurPoint += 1
			w = exp(-log(1+total_strain)) 		# Relative guage uniform width
			n = w
		# Stage 3 of curve
		elif self.s2_s3CurPoint <= self.s2_s3Points:
			pl_strain = self.EL*self.s2_s3CurPoint*self.s2_s3Inc
			stress = self.UTS-self.UTS_YS_diff*exp((pl_strain-self.ELmult)/self.ELfact) # Engineering Stress
			stress_true = self.UTS-self.UTS_YS_diff*exp(-pl_strain/self.ELfact) # True Stress
			tot_strain = stress/self.E
			total_strain = tot_strain+pl_strain
			self.s2_s3CurPoint += 1
			w = exp(-log(1+total_strain)) 						# Relative guage uniform width
			n = exp(-log(1+total_strain))*(stress/stress_true)	# Relative remaining neck width

		a = (w-n)*1.5 # relative elipse width
		b = 5*a		# ellipse height		
		if self.s2_s3CurPoint > self.s2_s3Points: # Check if simulation is done
			done = True		
		self.Xvals.append(total_strain) # Update graph
		self.Yvals.append(stress)
		return self.Xvals, self.Yvals, total_strain, w, a, b, done