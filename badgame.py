#Running code in linux comandline: python2 badgame.py
import pygame

pygame.init()

white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
 
 
 
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
			
			
	lead_x += lead_x_change
	lead_y += lead_y_change
	gameDisplay.fill(white)
	pygame.draw.rect(gameDisplay, red, [lead_x,lead_y,10, 40]) #(x,y,with,hight)
	pygame.draw.rect(gameDisplay, red, [lead_x + 10 ,lead_y + 40,20,20 ])
	pygame.draw.rect(gameDisplay, red, [lead_x - 20 ,lead_y + 40,20,20 ])
	
	pygame.display.update()
	clock.tick(30)
pygame.quit()
quit()
