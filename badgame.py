#Running code in linux comandline: python2 badgame.py
''' 1: git add badgame.py  
    2: git commit -m "message" 
    3: git push origin master'''
import pygame

pygame.init()

white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
tan   = (234,197,146)

def drawRoom():
	gameDisplay.fill(white)
	pygame.draw.rect(gameDisplay, tan, [50,50,700, 500])

def drawLead(lead_x, lead_y):
	
	pygame.draw.rect(gameDisplay, red, [lead_x,lead_y,10, 40]) #(x,y,with,hight)
	pygame.draw.rect(gameDisplay, red, [lead_x + 10 ,lead_y + 40,20,20 ])
	pygame.draw.rect(gameDisplay, red, [lead_x - 20 ,lead_y + 40,20,20 ]) 
	
def checkCollision(lead_x,lead_x_change, lead_y,lead_y_change):
	lead_x += lead_x_change
	lead_y += lead_y_change
	if lead_x >= 750-30 or lead_x <= 50 + 20:
		return True
	return False
 
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('pygamegame')

gameExit = False

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0
movLeft = False
movRight = False
movUp = False
movDown = False

clock = pygame.time.Clock()

while not gameExit:
	for event in pygame.event.get():
		#print(event)
		if event.type == pygame.QUIT:
			gameExit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				movLeft = True
				lead_x_change =  -10
			if event.key == pygame.K_RIGHT:
				movRight = True
				lead_x_change = 10
			if event.key == pygame.K_UP:
				movUp = True
				lead_y_change =  -10
			if event.key == pygame.K_DOWN:
				movDown = True
				lead_y_change = 10  
		
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:  
				lead_x_change = 0
				movLeft = False
				if movRight == True:
					lead_x_change = 10
					
			if event.key == pygame.K_RIGHT:
				lead_x_change = 0
				movRight = False
				if movLeft == True:
					lead_x_change = -10
			
			if event.key == pygame.K_UP:  
				lead_y_change = 0
				movUp = False
				if movDown == True:
					lead_y_change = 10
					
			if event.key == pygame.K_DOWN:
				lead_y_change = 0
				movDown = False
				if movUp == True:
					lead_y_change = -10
	
	
	
	collide = False		
	collide = checkCollision(lead_x,lead_x_change, lead_y,lead_y_change)
	drawRoom()
	
	
	if collide == False:
		lead_x += lead_x_change
		lead_y += lead_y_change
		drawLead(lead_x, lead_y)
	if collide == True:
		drawLead(lead_x, lead_y)
	
	
	pygame.display.update()
	clock.tick(30)
pygame.quit()
quit()
