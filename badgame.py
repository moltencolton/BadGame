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
	2: Create a way to have multipal doors in the same room linking to diffrent
	   places
	3: Create real sprites for lead charicter and floor/objects
	4: Working on making multipal stairs on a floor [0-4], there is some 
	   ground work for it but there still can only be one set. 
	
'''

import pygame
pygame.init()

white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
tan   = (234,197,146)

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
'''
	This is the Class that had to be created for Lead, instead
	of pushing around his location to every function, this lets
	him be an object that can be changed by methods globaly and 
	let us expand the data associated with him esially
'''	


class Create_Room_Sprite(pygame.sprite.Sprite):
	def __init__(self, image_file, location, Position, blink):
	        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
	        self.image = pygame.image.load(image_file)
	        self.rect = self.image.get_rect()
	        self.rect.left, self.rect.top = location
		self.doors = []
	def addStairs(self, doorPositions, link):
		if link != False:
			self.doors = [doorPositions, link]
		
'''
	this class was origanlly used just for creating and returning the room
	image after being correctly processed how java wants it.
	although this also became a great place to store elements of each room
	almost like a struct. having diffrent quordanates for each door position
	and what room that door links to. 
	
	there is a function in this class that adds a new set of stairs to the 
	room class, this is not working however and needs to be addressed,
	the function is called by currnetRoom.addStairs([array of door pos], room link)
	the array or doors pos is given in [x,y,whith,hight]
	
'''

def roomChange(lead, current_Room):
	if lead.x >= current_Room.doors[0][0] and lead.x <= (current_Room.doors[0][0] + current_Room.doors[0][2]) and lead.y >= current_Room.doors[0][1] and lead.y <= (current_Room.doors[0][1] + current_Room.doors[0][2]):
		lead.x = 300
		lead.y = 300
		return current_Room.doors[1]
	return current_Room
'''
	This function checks to see if the player is touching the stairs, 
	if the player is within the boundary of the stairs, it returns the 
	room that that stair leads too, if not, it returns the same room as
	was passed in
'''
	
def drawRoom(current_Room):
	gameDisplay.fill(white)
	gameDisplay.blit(current_Room.image, current_Room.rect)
	pygame.draw.rect(gameDisplay, tan, FLOOR_LIST)
	pygame.draw.rect(gameDisplay, black, current_Room.doors[0])
'''
	Does not need much explanation, function draws the room for 
	the "current_Room" that is passed into it. unsing calls to the class
'''
def drawLead(lead):
	pygame.draw.circle(gameDisplay,red, [lead.x, lead.y] , CHAR_BUFFER * 2, 0)
	
'''	
	OLD SPRITE, I drew a new one quickly so I could show this in public
	pygame.draw.rect(gameDisplay, red, [lead.x,lead.y,10, 40]) #(x,y,with,hight)
	pygame.draw.rect(gameDisplay, red, [lead.x + 10 ,lead.y + 40,20,20 ])
	pygame.draw.rect(gameDisplay, red, [lead.x - 20 ,lead.y + 40,20,20 ]) 
	
'''

def wallCollision(lead):
	lead.x_predict = lead.x + lead.x_change
	lead.y_predict = lead.y + lead.y_change
	if lead.x_predict >= current_Room.doors[0][0] and lead.x_predict <= (current_Room.doors[0][0] + current_Room.doors[0][2]) and lead.y_predict >= current_Room.doors[0][1] and lead.y_predict <= (current_Room.doors[0][1] + current_Room.doors[0][2]):
		lead.x += lead.x_change
		lead.y += lead.y_change
		return False
	if lead.x_predict >= (FLOOR_WITH + WALL_BUFFER - CHAR_BUFFER) or lead.x_predict <= (WALL_BUFFER + CHAR_BUFFER): 
		return True
	if lead.y_predict >= (FLOOR_HIGHT + WALL_BUFFER - CHAR_BUFFER) or lead.y_predict <= (WALL_BUFFER + CHAR_BUFFER):
		return True
	return False
	
'''
	This check wall function was our check colision function, but had to be 
	changed to adapt to exempt hitting the wall if a door was placed on that
	wall, also a lead.x and y predicted was added to look ahead a frame without
	adding lead_change to the movement yet. 
'''
 
gameDisplay = pygame.display.set_mode((800,600)) '''DO NOT CHANGE THIS NUMBER!!!'''
pygame.display.set_caption('pygamegame')

gameExit = False

lead = Lead
RoomEnd    = Create_Room_Sprite('wall16-800.jpg',[0,0], [0,0,0,0], False)
Room2_Wall = Create_Room_Sprite('green_crazy_circle-800x600.jpg', [0,0], [150,150,60,60], RoomEnd)
Room1_Wall = Create_Room_Sprite('background_image.jpg', [0,0], [0,450,50,60], Room2_Wall)
Room1_Wall.addStairs([500,200,60,60], Room2_Wall)
RoomEnd.addStairs([250,100,60,60],Room1_Wall)
Room2_Wall.addStairs([0,450,50,60], RoomEnd)

'''	This is just a test image that is passed to the class
	Background before real art can be made for the walls and such.
	more specific names need to be used
	syntax:
	Create_Room_Sprite('link to image' [0,0], [x,y,with,hight] for stairs, what room stairs lead)
	addStairs([x,y,with,hight],link to room object)
'''

movLeft = False
movRight = False
movUp = False
movDown = False
collide = False	

clock = pygame.time.Clock()
current_Room = Room1_Wall 

while not gameExit:
	drawRoom(current_Room)
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
		
		
	collide = wallCollision(lead)
	current_Room = roomChange(lead, current_Room)
	
	if collide == False:
		lead.x += lead.x_change
		lead.y += lead.y_change		
		drawLead(lead)
	if collide == True:
		drawLead(lead)
	
	
	pygame.display.update()
	clock.tick(30)
pygame.quit()
quit()
