'''
	Running code in linux comandline: python2 badgame.py
	1: git add badgame.py  
	2: git commit -m "message" 
	3: git push origin master
'''
'''
	MAIN NOTES! LIST OF THINGS THAT NEED TO BE DONE
	1: Code needs to start to be broken up into diffrent files for organization
	2: Fixing how the class is written. the class is not created properly to 
	   store all the information it does
	3: Create real sprites for lead charicter and floor/objects
	4: Make a Way to add more then one door in a room, this is a tough one!
'''

import pygame

pygame.init()

white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
tan   = (234,197,146)

FLOOR_LIST = [50,50,700,500]
CHAR_BUFFER = 5
WALL_BUFFER = FLOOR_LIST[0]
WALKING_SPEED = 8
FLOOR_HIGHT = FLOOR_LIST[3]
FLOOR_WITH  = FLOOR_LIST[2]

class Lead:
	x = 300
	y = 300
	x_change = 0
	y_change = 0

class Create_Room_Sprite(pygame.sprite.Sprite):
    def __init__(self, image_file, location, doorPosition, link):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.door = doorPosition
        if link != False:
        	self.doorLink = link
'''
	this class was origanlly used just for creating and returning the room
	image after being correctly processed how java wants it.
	although this also became a great place to store elements of each room
	almost like a struct. having diffrent quordanates for each door position
	and what room that door links to. 
		this class needs to be fixed to be much more elignet.
	Syntax:
	object.image returns image used for walls of room
	object.door returns the list of [x,y,with,hight] of the door (pos and size)
	object.doorLink returns what object (room) the stairs link to 
'''

def roomChange(lead, current_Room):
	if lead.x >= current_Room.door[0] and lead.x <= (current_Room.door[0] + current_Room.door[2]) and lead.y >= current_Room.door[1] and lead.y <= (current_Room.door[1] + current_Room.door[2]):
		lead.x = 300
		lead.y = 300
		return current_Room.doorLink
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
	pygame.draw.rect(gameDisplay, black, current_Room.door)
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
	lead.x += lead.x_change
	lead.y += lead.y_change
	if lead.x >= current_Room.door[0] and lead.x <= (current_Room.door[0] + current_Room.door[2]) and lead.y >= current_Room.door[1] and lead.y <= (current_Room.door[1] + current_Room.door[2]):
		return False
	if lead.x >= (FLOOR_WITH + WALL_BUFFER - CHAR_BUFFER) or lead.x <= (WALL_BUFFER + CHAR_BUFFER): 
		return True
	if lead.y >= (FLOOR_HIGHT + WALL_BUFFER - CHAR_BUFFER) or lead.y <= (WALL_BUFFER + CHAR_BUFFER):
		return True
	return False
	
'''
	Has not changed, except for changing numbers for Global variables
'''
 
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('pygamegame')

gameExit = False

lead = Lead
RoomEnd    = Create_Room_Sprite('wall16-800.jpg',[0,0], [0,0,0,0], False)
Room2_Wall = Create_Room_Sprite('green_crazy_circle-800x600.jpg', [0,0], [150,150,60,60], RoomEnd)
Room1_Wall = Create_Room_Sprite('background_image.jpg', [0,0], [0,450,50,60], Room2_Wall)

'''	This is just a test image that is passed to the class
	Background before real art can be made for the walls and such.
	more specific names need to be used
	syntax:
		Create_Room_Sprite('link to image' [0,0], [x,y,with,hight] for stairs, what room stairs lead)
'''

lead.x = 300
lead.y = 300
lead.x_change = 0
lead.y_change = 0
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
		lead.x -= lead.x_change
		lead.y -= lead.y_change
		drawLead(lead)
	
	
	pygame.display.update()
	clock.tick(30)
pygame.quit()
quit()
