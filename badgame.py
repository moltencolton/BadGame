'''
	Written by Aaron Statt and Colton Chambers

	Running code in linux comandline: python2 badgame.py
	1: git add badgame.py
	2: git commit -m "message"
	3: git push origin master
'''
'''
	MAIN NOTES! LIST OF THINGS THAT NEED TO BE DONE
	1: Code needs to start to be broken up into diffrent files for organization
	2: Create real sprites for lead charicter and floor/objects (Work being done on this)
	3: ONE MAJOR CHECK COLLISION FUNCTION THAT CAN TAKE PARAMITERS OR OBJECTS AND CHECK COLLISION T/F
	4: Collect all sprite images into one big image (like minecraft texture packs)
	3: Creating a goal for the game, items, enamies, and other objects
	4: Find way to shrink if statements
'''
''' 
	HOW TO PLAY!
	wasd for movement
	space to swing weapon
	i to open your bag
'''
import pygame, sys
from pygame.locals import *
pygame.init()

white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
tan   = (234,197,146)
green = (0  ,255,40 )

GAME_PAUSE = False
WALKING_SPEED = 15
FLOOR_LIST = [50,50,700,500]
FLOOR_HIGHT = FLOOR_LIST[3]
FLOOR_WITH  = FLOOR_LIST[2]
CHAR_BUFFER = 5
WALL_BUFFER = FLOOR_LIST[0]

class Lead:
	x = 300
	y = 300
	x_change = 0
	y_change = 0
	x_predict = 0
	y_predict = 0
	health = 100
	bag_weapons = [['Sword', 10, 25, 5] ]
	
	weapon = bag_weapons[0][0]
	damage = bag_weapons[0][1]
	weapon_width = bag_weapons[0][2]
	weapon_hight = bag_weapons[0][3]
	weapon_enabled = False
	
	
	def addWeapon(atributes):
		bag_weapons.append(atributes)
'''
	This is the Class that had to be created for Lead, instead
	of pushing around his location to every function, this lets
	him be an object that can be changed by methods globaly and
	let us expand the data associated width him esially
'''
class Create_Sprite(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
	        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		print self.rect
		self.rect.left, self.rect.top = location

class Create_Room_Sprite(pygame.sprite.Sprite):
	def __init__(self, image_file, location):
	        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.stairs = []
		self.links = []
		self.enemies = []
		self.enemyType = []
	def addStairs(self, doorPositions, link):
		if link != False:
			self.stairs.append(doorPositions)
			self.links.append(link)
    	def addEnemy(self, enemyPositions, kind):
		self.enemies.append(enemyPositions)	
		self.enemyType.append(kind)
'''
	enemyKind[0] = [color, type, size, health]
	
	this class was origanlly used just for creating and returning the room
	image after being correctly processed how java wants it.
	although this also became a great place to store elements of each room
	almost like a struct. having diffrent quordanates for each door position
	and what room that door links to.

	there is a function in this class that adds a new set of stairs to the
	room class, this is not working however and needs to be addressed,
	the function is called by currnetRoom.addStairs([array of door pos], room link)
	the array or stairs pos is given in [x,y,width,hight]
	len()

'''
def roomChange(lead, current_Room):
	for i in range(0, len(current_Room.stairs)):
		if lead.x >= current_Room.stairs[i][0] and lead.x <= (current_Room.stairs[i][0] + current_Room.stairs[i][2]) and lead.y >= current_Room.stairs[i][1] and lead.y <= (current_Room.stairs[i][1] + current_Room.stairs[i][2]):
			lead.x = 300
			lead.y = 300
			return current_Room.links[i]
	return current_Room
'''
	This function checks to see if the player is touching the stairs,
	if the player is within the boundary of the stairs, it returns the
	room that that stair leads too, if not, it returns the same room as
	was passed in.
	This for loop then cicles through all of the stairs making sure that
	the player can use all of them.
'''

def enemyCollision(lead, current_Room):
	for i in range(0, len(current_Room.enemies)):
		if lead.x >= (current_Room.enemies[i][0] - current_Room.enemyType[i][2]) and lead.x <= (current_Room.enemies[i][0] + current_Room.enemyType[i][2]) and lead.y >= (current_Room.enemies[i][1] - current_Room.enemyType[i][2]) and lead.y <= (current_Room.enemies[i][1] + current_Room.enemyType[i][2]):
			if current_Room.enemyType[i][3] > 0:
				lead.x = 300
				lead.y = 300
				lead.health -= 10
				if lead.health <= 0:
					return RoomEnd
			return current_Room
		if lead.weapon_enabled == True:
			if (lead.x + lead.weapon_width) >= (current_Room.enemies[i][0] - current_Room.enemyType[i][2]) and (lead.x + lead.weapon_width) <= (current_Room.enemies[i][0] + current_Room.enemyType[i][2]) and (lead.y + lead.weapon_hight) >= (current_Room.enemies[i][1] - current_Room.enemyType[i][2]) and (lead.y + lead.weapon_hight) <= (current_Room.enemies[i][1] + current_Room.enemyType[i][2]):	
				current_Room.enemyType[i][3] -= lead.damage
	return current_Room
'''
	This function checks to see if the player is touching an enemy,
	if the player is within the boundary of the enemy, it returns the
	room the original room and resets player position, if not, it returns the same room as
	was passed in.
	This for loop then cicles through all of the stairs making sure that
	the player can use all of them.
'''

def drawRoom(current_Room, lead, Stairs_Sprite):
	gameDisplay.fill(white)
	if current_Room == RoomEnd:
		gameDisplay.blit(current_Room.image, current_Room.rect)
		gameDisplay.blit(EndgameText, EndgameTextObject)	
		return 
	gameDisplay.blit(current_Room.image, current_Room.rect)
	pygame.draw.rect(gameDisplay, tan, FLOOR_LIST)
	pygame.draw.rect(gameDisplay, red, [20,20, lead.health, 15])
	
	for x in range(0, len(current_Room.stairs)):
		gameDisplay.blit(Stairs_Sprite.image, current_Room.stairs[x])
		
	drawEnemy(current_Room)
	
'''
	Does not need much explanation, function draws the room for
	the "current_Room" that is passed into it. unsing calls to the class
'''
def drawLead(lead):
	pygame.draw.circle(gameDisplay,red, [lead.x, lead.y] , CHAR_BUFFER * 2, 0)
	if lead.weapon_enabled == True:
		pygame.draw.rect(gameDisplay, black, [lead.x, lead.y, lead.weapon_width, lead.weapon_hight])
'''
	OLD SPRITE, I drew a new one quickly so I could show this in public
	pygame.draw.rect(gameDisplay, red, [lead.x,lead.y,10, 40]) #(x,y,width,hight)
	pygame.draw.rect(gameDisplay, red, [lead.x + 10 ,lead.y + 40,20,20 ])
	pygame.draw.rect(gameDisplay, red, [lead.x - 20 ,lead.y + 40,20,20 ])

'''
def drawEnemy(current_Room):
	for i in range(0, len(current_Room.enemies)):
		if current_Room.enemyType[i][3] >= 0:
			pygame.draw.circle(gameDisplay,current_Room.enemyType[i][0], [current_Room.enemies[i][0], current_Room.enemies[i][1]] , current_Room.enemyType[i][2], 0)

def wallCollision(lead):
	lead.x_predict = lead.x + lead.x_change
	lead.y_predict = lead.y + lead.y_change
	for i in range(0, len(current_Room.stairs)):
		if lead.x_predict >= current_Room.stairs[i][0] and lead.x_predict <= (current_Room.stairs[i][0] + current_Room.stairs[i][2]) and lead.y_predict >= current_Room.stairs[i][1] and lead.y_predict <= (current_Room.stairs[i][1] + current_Room.stairs[i][2]):
			return 0
	if (lead.x_predict >= (FLOOR_WITH + WALL_BUFFER - CHAR_BUFFER) or lead.x_predict <= (WALL_BUFFER + CHAR_BUFFER)) and (lead.y_predict >= (FLOOR_HIGHT + WALL_BUFFER - CHAR_BUFFER) or lead.y_predict <= (WALL_BUFFER + CHAR_BUFFER)):
		return 1
        if lead.x_predict >= (FLOOR_WITH + WALL_BUFFER - CHAR_BUFFER) or lead.x_predict <= (WALL_BUFFER + CHAR_BUFFER):
            	return 2
	if lead.y_predict >= (FLOOR_HIGHT + WALL_BUFFER - CHAR_BUFFER) or lead.y_predict <= (WALL_BUFFER + CHAR_BUFFER):
		return 3
	return 0

'''
	This check wall function was our check colision function, but had to be
	changed to adapt to exempt hitting the wall if a door was placed on that
	wall, also a lead.x and y predicted was added to look ahead a frame without
	adding lead_change to the movement yet.
	the for loop is added to check all of the stairs in the room.
'''
def dispWeaponText(lead):
	WeaponText = GuiFont.render(' Weapon : ' + lead.weapon + ' ' , True,red, tan)
	WeaponTextObject = WeaponText.get_rect()
	WeaponTextObject.center = (200, 10)	
	gameDisplay.blit(WeaponText, WeaponTextObject)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('pygamegame')

gameExit = False

lead = Lead
Stairs_Sprite = Create_Sprite('stairs.jpg',[0,0])
Bag_Sprite = Create_Sprite('bag.jpg', [100,100])
RoomEnd    = Create_Room_Sprite('wall16-800.jpg',[0,0])
Room2_Wall = Create_Room_Sprite('green_crazy_circle-800x600.jpg', [0,0])
Room1_Wall = Create_Room_Sprite('background_image.jpg', [0,0])
Room1_Wall.addStairs([500,200,60,60], Room2_Wall)
RoomEnd.addStairs([250,100,60,60],Room1_Wall)
Room2_Wall.addStairs([20,450,60,60], RoomEnd)
Room2_Wall.addStairs([400,450,60,60], Room1_Wall)
Room1_Wall.addEnemy([200,200], [white, 1, 30,50])

'''	This is just a test image that is passed to the class
	Background before real art can be made for the walls and such.
	more specific names need to be used
	syntax:
	Create_Room_Sprite('link to image' [0,0], [x,y,width,hight] for stairs, what room stairs lead)
	addStairs([x,y,width,hight],link to room object)
	Create_Sprite('link to image' [pos on display x, y])
'''
EndgameFont = pygame.font.SysFont('monospace',40) #SysFont creates a font object from pygame font objects
EndgameText = EndgameFont.render('Game Over!', True, black, tan)
EndgameTextObject=EndgameText.get_rect()
EndgameTextObject.center =(400,300)
'''
	Initilize font for the end game font object.
	EndgameFont.render('text to be shown', T/F Antialiasing, Color, background Color)
	SURFACER.center = (x,y) is the position of the text. 
'''
GuiFont = pygame.font.SysFont('monospace',10) #SysFont creates a font object from pygame font objects
HealthText = GuiFont.render(' Health ', True, black, tan)
HealthTextObject = HealthText.get_rect()
HealthTextObject.center = (40,10)




movLeft = False
movRight = False
movUp = False
movDown = False
collide = False
bag_open = False

clock = pygame.time.Clock()
current_Room = Room1_Wall

while not gameExit:
	drawRoom(current_Room,lead, Stairs_Sprite)
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				movLeft = True
				lead.x_change =  -WALKING_SPEED
			if event.key == pygame.K_RIGHT:
				movRight = True
				lead.x_change = WALKING_SPEED
			if event.key == pygame.K_UP:
				movUp = True
				lead.y_change =  -WALKING_SPEED
			if event.key == pygame.K_DOWN:
				movDown = True
				lead.y_change = WALKING_SPEED
			if event.key == pygame.K_SPACE:
				lead.weapon_enabled = True
			if event.key == pygame.K_i:
				if GAME_PAUSE == False:
					GAME_PAUSE = True
					bag_open = True
				elif GAME_PAUSE == True:
					GAME_PAUSE = False
					bag_open = False
				


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				lead.x_change = 0
				movLeft = False
				if movRight == True:
					lead.x_change = WALKING_SPEED

			if event.key == pygame.K_RIGHT:
				lead.x_change = 0
				movRight = False
				if movLeft == True:
					lead.x_change = -WALKING_SPEED

			if event.key == pygame.K_UP:
				lead.y_change = 0
				movUp = False
				if movDown == True:
					lead.y_change = WALKING_SPEED

			if event.key == pygame.K_DOWN:
				lead.y_change = 0
				movDown = False
				if movUp == True:
					lead.y_change = -WALKING_SPEED
			if event.key == pygame.K_SPACE:
				lead.weapon_enabled = False
				

	if GAME_PAUSE == False:
		dispWeaponText(lead)
		gameDisplay.blit(HealthText, HealthTextObject)
		collide = wallCollision(lead)
		current_Room = roomChange(lead, current_Room)
		current_Room = enemyCollision(lead, current_Room)
			
		if collide == 0:
			lead.x += lead.x_change
			lead.y += lead.y_change
			drawLead(lead)
		if collide == 1:
			drawLead(lead)
	    	if collide == 2:
	        	lead.y += lead.y_change
	        	drawLead(lead)
	    	if collide == 3:
	        	lead.x += lead.x_change
	        	drawLead(lead)
	if bag_open == True:
		gameDisplay.blit(current_Room.image, current_Room.rect)
		gameDisplay.blit(Bag_Sprite.image, Bag_Sprite.rect)
		
	
	pygame.display.update()
	clock.tick(30)
pygame.quit()
quit()
