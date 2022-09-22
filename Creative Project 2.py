###Plays Snake (Pwease gib eight owo)
import random

###User defined variables:
startSpeed = 2 #Amount of movements taken by the snake per second.
addedSpeed = .12 #Added to `startSpeed` per apple eaten.
maxSpeed = 5.5 #Speed will not increase if it's equal to or greater than this.
startSize = 4 #Snake starting size.
wallTeleport = True #Should the snake teleport to the other side of the screen or die hitting a wall?

defShape = Rect(0, 0, 400/25, 400/25, border="white", borderWidth=2, visible = False) #Default shape used to generate new snake parts. Visible value will be changed. You can make this anyting you want and the snake will try to work with it!

###Actual code:
#Setup:
scoreDigits = [[
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake0.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake1.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake2.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake3.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake4.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake5.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake6.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake7.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake8.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake9.png", 400, 380-280-26),
	],[
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake0.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake1.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake2.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake3.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake4.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake5.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake6.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake7.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake8.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake9.png", 400, 380-280-26),
	],[
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake0.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake1.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake2.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake3.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake4.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake5.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake6.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake7.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake8.png", 400, 380-280-26),
	Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/Snake9.png", 400, 380-280-26),
	]]
app.background = rgb(168, 198, 78) #Sets background
direction = Label("up", 400, 400, visible = False) #Creates the label that will later tell `move()` which direction to go.
lastMove = Label("", 400, 400, visible = False) #Copied from `direction` on every move.
score = Label("0", 400, 400, visible = False) #Similar to `direction`. Increases with `eat()`.
playArea = Rect(200, 400-20, 400-40, 280, border = rgb(60, 65, 44), borderWidth = 10, fill = None, align = "bottom") #The box that goes around the gameplay area. Purely cosmetic.
snakeShapes = [] #Setup for the numerically sorted snake pieces.
snake = Group() #All shapes within `snakeShapes` will be placed in this group. It exists mainly for its `hitTest()` method.
gameImage = Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/SnakeGame.png", 400, 400)
overImage = Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/SnakeOver.png", 400, 400)
titleImage = Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/SnakeLogo3.png",200-113,80) #The image displayed before the game starts. Setting it's `left` value to 400 will make the game start.
creditImage = Image("https://compsci-resources.s3.us-west-2.amazonaws.com/Snake/SnakeCredit3.png",200-(186/2), 140)
apple = Rect(400, 400, 10, 10, fill = rgb(60, 65, 44)) #Are we as the player supposed to be evil? Are we the ones who caused pain amongst humanity? Who knew.

def updateScoreboard():
	currentScore = score.value.zfill(3)
	for i in range(0, len(scoreDigits)):
		for x in scoreDigits[i]:
			x.left = 400
		scoreDigits[i][int(currentScore[i])].left = 400-((3-i)*2)-(((3-i))*12)-18
		
def endGame(): #Tony Stark dies.
	apple.visible = False
	for i in scoreDigits:
		for x in i:
			x.left = 400
	sleep(.1)
	gameImage.left, gameImage.top = 19, 78
	sleep(.5)
	overImage.left, overImage.top = 214, 78
	for i in range(0, len(snakeShapes)):
		snakeShapes[(len(snakeShapes)-i)-1].visible = False
		sleep(0)
	print("You're bad and you should feel bad.") #Entice the player to give it another go!
	app.stepsPerSecond = 0 #Stop the game loop.
	app.stop() #Kill the process altogether.
	
def moveApple(): #It's in the name.
	randomLeft, randomTop = (random.randrange(1,21)*16)+34+1, (random.randrange(1,16)*16)+114+1 
	apple.left, apple.top = randomLeft, randomTop #Move `apple` to a random location on the grid
	if snake.hitTest(randomLeft, randomTop): #Make sure the apple doesn't move on top of the snake.
		moveApple()
	
def makeSnake(): #Makes the starting snake parts.
	snakeShapes.append(Rect(200, 200, 400/25-2, 400/25-2, fill = rgb(60, 65, 44), align = "center", border = rgb(168, 198, 78), borderWidth = 1)) #Create the first rectangle.
	genParts(startSize-1) #A Snake is Born (2018)
	moveApple() #Get the apple ready for consumption
	updateScoreboard()
	
def genParts(amount): #Adds length to the snake. Use `amount` to change how many squares you want added.
	for i in range(0, amount): #Iterate through `amount` times
		lastShape = snakeShapes[len(snakeShapes)-1] #Get the last shape in the snake for use as a reference
		snakeShapes.append(Rect(lastShape.left, lastShape.top, lastShape.width, lastShape.height, fill = rgb(60, 65, 44), border = rgb(168, 198, 78), borderWidth = 1)) #Use the properties of 'lastShape' to create a new part of the snake, making it longer.
		for x in snakeShapes: #Iterate through every item in `snakeShapes`
			snake.add(x) #Add the item currently being looked at by the for loop to the `snake` group.
	
def move(facing): #Move the tail of the snake to the head based off of `facing`.
	lastShape = snakeShapes[len(snakeShapes)-1] #Bind the current last rectangle in `snakeShapes`.
	firstShape = snakeShapes[0] #Bind the current first rectangle in `snakeShapes`.
	#The first of many long lists of elifs. Creates offsets based off of the current desired direction.
	if facing == "up":
		topOffset, leftOffset = firstShape.top - 16, firstShape.left
	elif facing == "left":
		topOffset, leftOffset = firstShape.top, firstShape.left - 16
	elif facing == "down":
		topOffset, leftOffset = firstShape.top + 16, firstShape.left
	elif facing == "right":
		topOffset, leftOffset = firstShape.top, firstShape.left + 16
	prevLocTop, PrevLocLeft = lastShape.top, lastShape.left
	lastShape.top, lastShape.left = 400, 400
	if snake.hitTest(leftOffset, topOffset): #Skip moving and return false if the snake will hit itself on move.
		lastShape.top, lastShape.left = prevLocTop, PrevLocLeft
		return(False)
	lastMove.value = facing
	lastShape.top, lastShape.left = topOffset, leftOffset #Move the shape to the offset points defined in the if statement above.
	lastShape.borderWidth = 1 #Reset the borders in case this part of the snake was used to eat the `apple`.
	snakeShapes.insert(0, snakeShapes.pop(len(snakeShapes)-1)) #Relocate the shape within `snakeShapes` in order to serve futer `move()` functions.
	return(True)
	
def eat(): #5
	score.value = str(int(score.value)+1) #What is life without something to show for it?
	snakeShapes[0].borderWidth = 0 #Create the illusion of digestion by making this part of the snake fatter. Since this shape will stay in the same place, it will seem as if it is moving through the snake's body.
	genParts(1) #Add another part to the snake
	moveApple() #Because we need challenge.
	if app.stepsPerSecond < maxSpeed:
		app.stepsPerSecond = app.stepsPerSecond + addedSpeed #Speed up the game to make it more tense.
	updateScoreboard()
	
def onKeyPress(key): #Manages keypresses and their functions:
	if titleImage.left == 200-113: #Start the game if `titleImage` is in it's starting location:
		titleImage.left = 400 #Move `titleImage` so that it's no longer visible.
		creditImage.left = 400 #Same thing for credits
		makeSnake() #Finally!
		app.stepsPerSecond = startSpeed #Start the game loop
	#Long list of elifs that changes `direction.value` based off of keypresses:
	if key == "w" or key == "up":
		if lastMove.value == "down":
			return
		direction.value = "up"
	elif key == "a" or key == "left":
		if lastMove.value == "right":
			return
		direction.value = "left"
	elif key == "s" or key == "down":
		if lastMove.value == "up":
			return
		direction.value = "down"
	elif key == "d" or key == "right":
		if lastMove.value == "left":
			return
		direction.value = "right"
		
if wallTeleport == False:
	def wallAction(snakeHead):
		if snakeHead.top <= 113 and direction.value == "up":
			endGame()
			return(False)
		elif snakeHead.top >= 354-16 and direction.value == "down":
			endGame()
			return(False)
		elif snakeHead.left <= 34 and direction.value == "left":
			endGame()
			return(False)
		elif snakeHead.left >= 354-16 and direction.value == "right":
			endGame()
			return(False)
if wallTeleport == True:
	def wallAction(snakeHead):
		if snakeHead.top <= 113 and direction.value == "up":
			snakeShapes[len(snakeShapes)-1].top, snakeShapes[len(snakeShapes)-1].left = 353, snakeShapes[0].left
			snakeShapes.insert(0, snakeShapes.pop(len(snakeShapes)-1))
			return("Skip")
		elif snakeHead.top >= 354-16 and direction.value == "down":
			snakeShapes[len(snakeShapes)-1].top, snakeShapes[len(snakeShapes)-1].left = 113, snakeShapes[0].left
			snakeShapes.insert(0, snakeShapes.pop(len(snakeShapes)-1))
			return("Skip")
		elif snakeHead.left <= 34 and direction.value == "left":
			snakeShapes[len(snakeShapes)-1].left, snakeShapes[len(snakeShapes)-1].top = 353, snakeShapes[0].top
			snakeShapes.insert(0, snakeShapes.pop(len(snakeShapes)-1))
			return("Skip")
		elif snakeHead.left >= 354-16 and direction.value == "right":
			snakeShapes[len(snakeShapes)-1].left, snakeShapes[len(snakeShapes)-1].top = 33, snakeShapes[0].top
			snakeShapes.insert(0, snakeShapes.pop(len(snakeShapes)-1))
			return("Skip")
		
###Game Loop:
app.stepsPerSecond = 0
def onStep(): #Runs every step:
	if titleImage.left == 400: #Wait for the game to start. See more in `onKeyPress`
		snakeHead = snakeShapes[0] #Find the front of the snake for use in collision tracking.
		doMove = wallAction(snakeHead)
		if doMove == False: return #Stop the game if the snake will hit a wall.
		elif doMove == "Skip":
			print("Teleported")
		else:
			if move(direction.value) == False: endGame() #Pass direction to `move()` and check for collision with snake.
		if apple.hitsShape(snakeShapes[0]): eat() #Gobble down that apple!