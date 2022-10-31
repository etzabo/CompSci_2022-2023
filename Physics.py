from cmu_graphics import *
import math
import numpy as np
from itertools import combinations
import warnings

def closest(list, value):
	list = np.asarray(list)
	return list[np.abs(list - value).argmin()]

class Physics():
	particles = []
	stationaries = []
	def handleCollisions():
		pairs = combinations(Physics.particles, 2)
		for i,j in pairs:
			if i.overlaps(j):
				j.shape.centerX -= int(j.v[0])/app.stepsPerSecond
				j.shape.centerY -= int(j.v[1])/app.stepsPerSecond
				
				m1, m2 = i.shape.radius**2, j.shape.radius**2
				M = m1 + m2
				r1, r2 = np.array([i.shape.centerX, i.shape.centerY]), np.array([j.shape.centerX, j.shape.centerY])
				d = np.linalg.norm(r1 - r2)**2
				v1, v2 = i.v, j.v
				u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
				u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
				i.v = u1
				j.v = u2
		for i in Physics.stationaries:
			for j in Physics.particles:
				overlaps, colPoint = i.overlaps(j)
				if overlaps:
					j.shape.centerX -= int(j.v[0])/app.stepsPerSecond
					j.shape.centerY -= int(j.v[1])/app.stepsPerSecond
					
					jMid = np.array([j.shape.left+(j.shape.width/2), j.shape.top+(j.shape.height/2)]) #Edit this to add non axis-aligned rectangle support.
					iMid = np.array([i.shape.centerX, i.shape.centerY])
					
					cornerPoints = [np.array([i.shape.left, i.shape.top]), np.array([i.shape.left+i.shape.width, i.shape.top]), np.array([i.shape.left, i.shape.top+i.shape.height]), np.array([i.shape.left+i.shape.width, i.shape.top+i.shape.height])]
					
					for x in cornerPoints:
						if int(colPoint[0]) == int(x[0]) and int(colPoint[1]) == int(x[1]):
							m1, m2 = 1, j.shape.radius**2
							M = m1 + m2
							r1, r2 = x, np.array([j.shape.centerX, j.shape.centerY])
							d = np.linalg.norm(r1 - r2)**2
							v1, v2 = j.v, 0
							u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
							j.v = u1
							return()
					
					m1, m2 = 1, j.shape.radius**2
					M = m1 + m2
					r1, r2 = colPoint, np.array([j.shape.centerX, j.shape.centerY])
					d = np.linalg.norm(r1 - r2)**2
					v1 = j.v
					u1 = v1 - 2*m2 / M * np.dot(v1, r1-r2) / d * (r1 - r2)
					j.v = u1

class Particle():
	def __init__(self, shape, vx = 0, vy = 0, autoSim = True):
		if not isinstance(shape, Circle):
			warnings.warn("Instance is not of Circle class. There may be issues when referencing attributes associated with Circle.")
		self.shape = shape
		self.v = np.array((vx, vy))
		if autoSim:
			Physics.particles.append(self)
		
	def move(self):
		try: self.shape.centerX += int(self.v[0])/app.stepsPerSecond
		except ValueError: self.v = np.array([100, 100])
		
		try: self.shape.centerY += int(self.v[1])/app.stepsPerSecond
		except ValueError: self.v = np.array([100, 100])
		
	def overlaps(self, p2):
		p1 = self
		r1 = np.array([p1.shape.centerX, p1.shape.centerY])
		r2 = np.array([p2.shape.centerX, p2.shape.centerY])
		
		print(np.linalg.norm(r1-r2))
		
		return(np.linalg.norm(r1-r2) <= self.shape.radius + p2.shape.radius)

class Stationary():
	def __init__(self, shape, vMultiplier = 1, autoSim = True):
		if not isinstance(shape, Rect):
			warnings.warn("Instance is not of Rect class. There may be issues when referencing attributes associated with Rect.")
		self.shape = shape
		self.vMultiplier = vMultiplier
		if autoSim:
			Physics.stationaries.append(self)
	
	def overlaps(self, p2):
		p1 = self
		rectPoint = np.array([max(self.shape.left, min(p2.shape.centerX, self.shape.left + self.shape.width)), max(self.shape.top, min(p2.shape.centerY, self.shape.top + self.shape.height))])
		circPoint = np.array([p2.shape.centerX, p2.shape.centerY])
		
		return([np.linalg.norm(rectPoint-circPoint) <= p2.shape.radius^2, rectPoint])
  ########################################################################################
### +----------------------------------------------------------------------------------+ ###
### |DO NOT EDIT ABOVE. MAKE OBJECTS WITH Particle(shape, vx, vy) and Stationary(shape)| ###
### +----------------------------------------------------------------------------------+ ###
  ########################################################################################

def beforeStep():
	pass

for i in range(0, 20):
	Particle(Circle(200, i*10+100, 10), vx = -1000, vy = 5)

leftBound = Stationary(Rect(-100, 0, 100, 400))
topBound = Stationary(Rect(0, -100, 400, 100))
rightBound = Stationary(Rect(400, 0, 100, 400))
bottomBound = Stationary(Rect(0, 400, 400, 100))

rectangle = Stationary(Rect(200, 200, 100, 150))

debugLine = Line(0,0,0,0,fill=rgb(0, 255, 0))

def afterStep():
	pass

  ########################################################################################
### +----------------------------------------------------------------------------------+ ###
### |DO NOT EDIT BELOW. A SYSTEM WILL BE ADDED TO CREATE FUNCTIONS THAT RUN EVERY STEP.| ###
### +----------------------------------------------------------------------------------+ ###
  ########################################################################################
app.stepsPerSecond = 30
def onStep():
	beforeStep()
	for x in Physics.particles:
		x.move()
	Physics.handleCollisions()
	afterStep()

cmu_graphics.run()