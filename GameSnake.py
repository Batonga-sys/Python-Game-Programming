# Game : Snake


from pathlib import Path
import pygame
import time
import random
pygame.init()



#COLOURS
WHITE     = (255, 255, 255)
BLACK     = (0  , 0  , 0  )
RED       = (255, 0  , 0  )
GREEN     = (0  , 255, 0  )
BLUE      = (0  , 0  , 255)
DARKGREEN = (0  , 155, 0  )
blue_ciel   =   (119, 181 , 254)
Brown = (139, 69 , 19)


#set
str(Path('set/'))
img_SnakeHead = pygame.image.load(str(Path('set/SnakeHead.png')))
img_Apple     = pygame.image.load(str(Path('set/Apple.png')))
img_Icon      = pygame.image.load(str(Path('set/SnakeIcon.png')))


#GAME WINDOW
display_width  = 800
display_height = 650
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("SNAKE PROJET")
pygame.display.set_icon(img_Icon)
pygame.display.update()
clock = pygame.time.Clock()
fps = 20


# L'écran d'accueil/ SCREEN
ScreenSnake = pygame.image.load(str(Path('set/OpenSnake.png')))
ScreenSnake = pygame.transform.scale(ScreenSnake,(800,650))


def game_opening():
    gameDisplay.blit(ScreenSnake, (0,0))
    pygame.display.update()
    time.sleep(3)
game_opening()



#START SCREEN
def game_intro():
    intro = True
    while intro:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                intro = False
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
        
        gameDisplay.fill(WHITE)
        message_to_screen("Welcome to Snake!",
                          colour = GREEN,
                          y_displace = -100,
                          size = "large")
        message_to_screen("L'objectif du jeu est de manger les pommes rouges",
                          colour = BLACK,
                          y_displace = -30)
        message_to_screen("Plus le serpent mange de pommes, plus il devient long! Haha",
                          colour = BLACK,
                          y_displace = 10)
        message_to_screen("mais si il se heurte au bord ou à lui-meme, il meurt!.",
                          colour = BLACK,
                          y_displace = 50)
        message_to_screen(" Ctrl J pour jouer, Ctrl P pour mettre en pause or Ctrl Q pour quitter",
                          colour = BLACK,
                          y_displace = 180)
                          
        pygame.display.update()
        #clock.tick(15)

#PAUSE FUNCTION
def pause():
    
    paused = True
    
    message_to_screen("En pause!",
                      BLACK,
                      -100,
                      size = "large")
    message_to_screen("Appuyer sur ctrl j pour continuer ou ctrl q pour quitter",
                      BLACK,
                      30)
                      
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        clock.tick(15)
        
#SCORE FUNCTION
def score(score):       
    text = smallfont.render("Score: "+str(score), True, BLACK)
    gameDisplay.blit(text, [10,10])
    
#APPLE COORDINATES FUNCTION     
def randAppleGen(borderSize, objectSize):
    randAppleX = round(random.randrange(borderSize, display_width  - (objectSize + borderSize))) #/10.0)*10.0
    randAppleY = round(random.randrange(borderSize, display_height - (objectSize + borderSize))) #/10.0)*10.0
    return randAppleX, randAppleY
    
#SNAKE FUNCTION
direction = 'right'
def snake(lead_width, lead_height, snakeList):
    if direction == 'right':
        head = pygame.transform.rotate(img_SnakeHead, 270)
        
    if direction == 'left':
        head = pygame.transform.rotate(img_SnakeHead, 90)
        
    if direction == 'up':
        head = img_SnakeHead
        
    if direction == 'down':
        head = pygame.transform.rotate(img_SnakeHead, 180)
    
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, DARKGREEN, [XnY[0],XnY[1], lead_width,lead_height])


#TEXT FUNCTIONS
smallfont = pygame.font.SysFont("Times New Roman", 25)
medfont   = pygame.font.SysFont("Times New Roman", 50)
largefont = pygame.font.SysFont("Times New Roman", 80)
def text_objects(text, colour, size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    elif size == "medium":
        textSurface = medfont.render(text, True, colour)
    elif size == "large":
        textSurface = largefont.render(text, True, colour)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg, colour, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    
    #GAME CONDITIONS
    gameExit = False
    gameOver = False
    
    
    #SNAKE VARIABLES
    lead_x         = display_width/2
    lead_y         = display_height/2
    lead_width     = 20
    lead_height    = 20
    lead_x_change  = 1
    lead_y_change  = 0
    block_change   = 10
    border         = 10
    snakeList      = []
    snakeLength    = 1
    appleThickness = 20
    global direction
    
    #INITIAL APPLE VARIABLES
    randAppleX, randAppleY = randAppleGen(border, appleThickness)
    
    #MAIN LOOP
    while not gameExit:
    
        #GAMEOVER PROMPT
        if gameOver == True:
            pygame.mixer.Sound('3275.mp3').play()
            message_to_screen("Jeu terminé!", 
                              RED,
                              y_displace = -50,
                              size = "large")
            message_to_screen(" appuyez sur Ctrl J pour rejouer ou Ctrl Q pour quitter.", 
                              BLACK, 
                              y_displace = +50,
                              size = "small")
            pygame.display.update()
        
        while gameOver == True:
                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_j:
                        direction = 'right'
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
            


        #KEYPRESS EVENTS
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if direction == 'right':
                        continue
                    lead_x_change = -block_change
                    lead_y_change =  0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    if direction == 'left':
                        continue
                    lead_x_change =  block_change
                    lead_y_change =  0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    if direction == 'down':
                        continue
                    lead_y_change = -block_change
                    lead_x_change =  0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    if direction == 'up':
                        continue
                    lead_y_change =  block_change
                    lead_x_change =  0
                    direction = 'down'
                elif event.key == pygame.K_p:
                    pause()
                    
            #QUIT EVENT
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True


                
        #WALL COLLISION
        if lead_x >= display_width -lead_width or lead_x <= 0 or lead_y >= display_height -lead_height or lead_y <= 0:
            gameOver = True
            
        #SNAKE MOVEMENT
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        #GAME WINDOW
        gameDisplay.fill(blue_ciel)
        pygame.draw.rect(gameDisplay, Brown, [0,0, display_width,display_height], border)
        gameDisplay.blit(img_Apple, (randAppleX, randAppleY))
        
        #SNAKE LENGTH
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        
        if len(snakeList) > snakeLength:
            del snakeList[0]
        
        #SELF COLLISION
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        
        snake(lead_width, lead_height, snakeList)
        
        score(snakeLength-1)
        
        #APPLE COLLISION/RESET
        if lead_x >= randAppleX and lead_x <= randAppleX +appleThickness or lead_x +block_change >= randAppleX and lead_x +block_change <= randAppleX +appleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY +appleThickness:
                randAppleX, randAppleY = randAppleGen(border, appleThickness)
                snakeLength += 1
            elif lead_y +block_change >= randAppleY and lead_y +block_change <= randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen(border, appleThickness)
                snakeLength += 1
            
        pygame.display.update()
        
        clock.tick(fps)
    #GAMEOVER MESSAGE
    pygame.display.update()
    pygame.quit()
    quit()

# MUSIC
pygame.mixer.music.load("Music.mp3")
pygame.mixer.music.play()
#GAME
game_intro()    
gameLoop()
