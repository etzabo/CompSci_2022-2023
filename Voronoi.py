import sys
import math
import random
import itertools
import copy

#########################
### DO NOT EDIT ABOVE ###
#########################

redrawOnDrag = True

# Debug and Visualization:
convexHullBorder = True

#########################
### DO NOT EDIT BELOW ###
#########################

cellDivision = 40
class LineBank:
    def __init__(self):
        self.stored = []
        self.export = []
    
    def withdraw(self):
        try:
            item = self.stored.pop(0)
        except:
            item = Line(-400, -400, -400, -400)
        
        item.visible = True
        
        self.export.append(item)
        return(item)
    
    def repack(self):
        for i in self.export:
            i.visible = False
            self.stored.append(i)
        
        self.export.clear()

lineBank = LineBank()

points = []
class Point:
    def __init__(self, x, y):
        self.shape = Circle(x, y, 6, fill = gradient(rgb(0, 0, 0), rgb(255, 255, 255), start = "center"), opacity = 50)
        self.distanceRelations = None
        points.append(self)

debugButtons = []
class DebugButton:
    def __init__(self, name, onFunc, offFunc, onColor = rgb(0, 255, 0), offColor = rgb(255, 0, 0)):
        self.shape = Rect(20+40*len(debugButtons), 400, 40, 20, align = "left-bottom")
        self.onFunc = onFunc
        self.offFunc = offFunc
        self.onColor = onColor
        self.offColor = offColor

### Mathematics:
def fixCmuY(y): # Translates the Y coordinate of a CMU shape to that of a more standardized form.
    return(abs(y-400))

def distance(p, q): # Edit this function to modify the distance between points! This will be called whenever a point is moved for each point in its cell until it has received the two closest points.
    return(math.dist([p[0], p[1]], [q[0], q[1]]))

def baseRound(x, base):
    return base * pythonRound(x/base)

def firstDivisor(n, start = 2): # Gets divisors of `n`. Automatically converts `n` to integer.
    n = int(n)
    for i in range(start, n):
        if n % i == 0: return(i)
    
    return(1) # If no divisors found, return 1.
    
def polarAngle(p, q):
    if p[1] == q[1]: # Avoid divide by zero error
        return(float("inf"))
    
    run = p[0] - q[0]
    rise = p[1] - q[1]
    return(-run/rise)

def getMatrixMinor(m, i, j):
    return([row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])])

def determinant(m):
    # Dec 8, 9:30: AAAAAAAAAAAAAAAAAAAAHHHAHHAHAHHHAHHAHHH WHYYYYYYYy NOOOOO PLEASE!!!
    # Dec 8, 12:51: I'm glad I'll never have to visit or edit this function ever again.
    
    if len(m) == 2:
        return(m[0][0]*m[1][1]-m[0][1]*m[1][0])
    
    product = 0
    for c in range(len(m)):
        product += ((-1)**c)*m[0][c]*determinant(getMatrixMinor(m, 0, c))
    
    return(product)

def convexHull(points):
    testPoints = points.copy()
    startPoint = testPoints[0]
    startIndex = 0
    for i in range(0, len(testPoints)): # Get the lowest point on the grid. If two candidates have the same Y value, choose the rightmost.
        testPoint = testPoints[i]
        testX, testY = testPoint.shape.centerX, testPoint.shape.centerY
        startX, startY = startPoint.shape.centerX, startPoint.shape.centerY
        if testY >= startY:
            if testY > startY:
                startPoint = testPoint
                startIndex = i
            elif testX > startX:
                startPoint = testPoint
                startIndex = i
    
    testPoints.pop(startIndex).shape.fill = rgb(255, 0, 0)
    testPoints = sorted(testPoints, key = lambda point: polarAngle([startPoint.shape.centerX, fixCmuY(startPoint.shape.centerY)], [point.shape.centerX, fixCmuY(point.shape.centerY)]))
    hullPoints = [startPoint, testPoints[0]]
    for i in range(1, len(testPoints)):
        if determinant([[hullPoints[-2].shape.centerX, fixCmuY(hullPoints[-2].shape.centerY), 0], [hullPoints[-1].shape.centerX, fixCmuY(hullPoints[-1].shape.centerY), 0], [testPoints[i].shape.centerX, fixCmuY(testPoints[i].shape.centerY), 0]]) >= 0:
            while determinant([[hullPoints[-2].shape.centerX, hullPoints[-1].shape.centerX, testPoints[i].shape.centerX], [fixCmuY(hullPoints[-2].shape.centerY), fixCmuY(hullPoints[-1].shape.centerY), fixCmuY(testPoints[i].shape.centerY)], [1, 1, 1]]) < 0:
                if len(hullPoints) <= 2:
                    break
                hullPoints.pop(-1).shape.fill = rgb(0, 255, 0)
            hullPoints.append(testPoints[i])
    
    for i in testPoints:
        i.shape.fill = rgb(0, 255, 0)
    
    for i in hullPoints:
        i.shape.fill = rgb(255, 0, 0)
    
    startPoint.shape.fill = rgb(0, 0, 255)
    
    return(hullPoints)

### Miscellaneous:

def nearPoints(point): # Determines which cell a point is in as well as its closest `closestAmount` points in order based on `mergeSort()`.
    for i in points:
        pass

### Redraw:
def redraw():
    try: clickedPoint.shape
    except: return
    
    nearPoints(clickedPoint)
    hull = convexHull(points)
    
    if convexHullBorder == True:
        lineBank.repack()
        for i in range(0, len(hull)):
            pulledLine = lineBank.withdraw()
            pulledLine.x1, pulledLine.y1, pulledLine.x2, pulledLine.y2 = hull[i].shape.centerX, hull[i].shape.centerY, hull[i-1].shape.centerX, hull[i-1].shape.centerY

if redrawOnDrag == True:
    def dragRedraw(): redraw()
    def onMouseRelease(mouseX, mouseY): pass
else:
    def dragRedraw(): pass
    def onMouseRelease(mouseX, mouseY): redraw()

def onMousePress(mouseX, mouseY):
    global clickedPoint
    clickedPoint = None
    for i in points:
        if i.shape.radius > math.dist([i.shape.centerX, i.shape.centerY], [mouseX, mouseY]):
            clickedPoint = i
            break

def onMouseDrag(mouseX, mouseY):
    try:
        clickedPoint.shape
    except:
        return
    
    clickedPoint.shape.centerX, clickedPoint.shape.centerY = mouseX, mouseY
    
    dragRedraw()
    
    
for i in range(10):
    Point(random.randrange(10, 390), random.randrange(10, 390))

#print(intSort([7, 8, 9, 9, 1, 6, 400, 99, 400, 1, 10, 11, 0, 20, 400], 400))
