import pygame, sys, random, math
from pygame.locals import *

class Ball: 
    """ 
        defines the Ball that will bounce
    """
    def __init__(self, radius, color, (x,y)) :
        self.radius = radius
        self.color = color 
        self.speedx = 0 
        self.speedy = 0 
        self.x, self.y = (x, y)
        self.reducey = 0 
        self.show = 1 

    def move(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy 

#some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)                                                                                                                         

#other constants
width = 1200 
height = 680
FPS = 60

#global variables
ballActiveList = []
bombs = []
bombsText = []
ballSizeMax = 20
ballSizeMin = 10
colors = [ GREEN, YELLOW ] 
gravity = 7
isMouseDown = 0
lastMouseX = 0
lastMouseY = 0
curMouseX = 0
curMouseY = 0
SCORE = 0
COLLISION = 0

pygame.init()
DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption("BALL CUT")
DISPLAYSURF.fill(WHITE)

mainWindow = pygame.Rect(15,15,width - 30, height - 30)
originRectOfBalls = pygame.Rect(width/2 - 100, height - 30, 190, 30)
fpsClock = pygame.time.Clock()

def initialize() :
    global ballActiveList, bombs, bombsText, isMouseDown, lastMouseX, lastMouseY, curMouseX, curMouseY, SCORE, COLLISION
    ballActiveList = []
    bombs = []
    bombsText = []
    isMouseDown = 0
    lastMouseX = 0
    lastMouseY = 0
    SCORE = 0
    COLLISION = 0
    curMouseX = 0
    curMouseY = 0

def getCrossProduct( A, B ):
    Ax, Ay = A
    Bx, By = B
    return Ay*Bx - Ax*By

def getMod( A, B ):
    x1, y1 = A
    x2, y2 = B
    return math.sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )

def distPerpendicular(X1, X2, X3):
    x1, y1 = X1
    x2, y2 = X2
    x3, y3 = X3
    return math.fabs( getCrossProduct( (x1-x2, y1-y2) , (x3-x2, y3-y2) ) / getMod( (x3, y3), (x2, y2) ))

def checkAngles(X1, X2, X3):
    x1, y1 = X1
    x2, y2 = X2
    x3, y3 = X3
    if getMod((x3,y3), (x2,y2))*getMod((x1,y1),(x2,y2)) == 0 : 
        theta1 = math.pi  
    else:
        theta1 = math.acos(float((x1-x2)*(x3-x2) + (y1-y2)*(y3-y2)) / float(getMod((x3,y3), (x2,y2))*getMod((x1, y1),(x2,y2))))
    
    if getMod((x1,y1), (x3,y3))*getMod((x2,y2),(x3,y3)) == 0 :
        theta2 = math.pi
    else:
        theta2 = math.acos(float((x1-x3)*(x2-x3) + (y1-y3)*(y2-y3)) / float(getMod((x1,y1), (x3,y3))*getMod((x2,y2), (x3,y3))))

    if theta1 <= math.pi / 2 and theta2 <= math.pi / 2 and theta1 >= 0 and theta2 >= 0:
        return True
    else:
        return False

def generateNewBall() :
    radius = random.randint(ballSizeMin, ballSizeMax)
    center = ( originRectOfBalls.centerx, originRectOfBalls.centery)
    newBall = Ball(radius, colors[random.randint(1,2) - 1], center)
    newBall.speedy = -1*random.randint(10, 17)
    newBall.speedx = random.randint(-6, 6)
    ballActiveList.append(newBall)

def generateBomb() :
    radius = random.randint(ballSizeMin, ballSizeMax)
    center = (originRectOfBalls.centerx, originRectOfBalls.centery)
    newBall = Ball(radius, BLUE, center)
    newBall.speedy = -1*random.randint(10,15)
    newBall.speedx = random.randint(-5, 5)
    bombs.append(newBall)
    bombFontObj = pygame.font.Font(None, int(3/2*radius))
    bombTextSurfaceObj = bombFontObj.render('B', True, RED, BLUE)
    bombTextRectObj = bombTextSurfaceObj.get_rect()
    bombTextRectObj.center = (newBall.x, newBall.y)
    bombsText.append( [bombTextSurfaceObj, bombTextRectObj])

def genNewBombAndBall():
    del ballActiveList[:]
    del bombs[:]
    del bombsText[:]

    numOfBalls = random.randint(2, 5)
    numOfBombs = random.randint(0, 3)

    for i in range(0, numOfBalls):
        generateNewBall()
    for i in range(0, numOfBombs):
        generateBomb()

def endGame():
    DISPLAYSURF.fill(BLACK)
    pygame.draw.rect(DISPLAYSURF, BLUE, mainWindow)
    endFontObj = pygame.font.Font(None, 50)
    endTextSurfaceObj = endFontObj.render('GAME OVER', True, WHITE, BLUE)
    endTextRectObj = endTextSurfaceObj.get_rect()
    endTextRectObj.center = (width/2, height/3) 
    
    scoreFontObj = pygame.font.Font(None, 40)
    scoreTextSurfaceObj = scoreFontObj.render('Score = %d  Press r to replay' %(SCORE), True, WHITE, BLUE)
    scoreTextRectObj = scoreTextSurfaceObj.get_rect()
    scoreTextRectObj.center = (width/2, height/2)

    DISPLAYSURF.blit(scoreTextSurfaceObj, scoreTextRectObj)
    DISPLAYSURF.blit(endTextSurfaceObj, endTextRectObj) 
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_r :
            initialize()
            print "GAME INITIALIZED"
 
print "GAME INITIALIZED"

while True:
    if COLLISION >= 3:
        endGame()
    else:
        scoreFontObj = pygame.font.Font(None, 40)
        scoreTextSurfaceObj = scoreFontObj.render('Score = %d' %(SCORE), True, BLUE, GREEN)
        scoreTextRectObj = scoreTextSurfaceObj.get_rect()
        scoreTextRectObj.center = (int(width/8), 16)

        collisionFontObj = pygame.font.Font(None, 40)
        collisionTextSurfaceObj = collisionFontObj.render('Collision = %d' %(COLLISION), True, BLUE, GREEN)
        collisionTextRectObj = collisionTextSurfaceObj.get_rect()
        collisionTextRectObj.center = (int((3*width)/4), 16)

        for ball in ballActiveList:
            if ball.y <= height + 10000:
                break
        else:
            genNewBombAndBall()

        for ball in bombs:
            if ball.y <= height + 10000:
                break
        else:
            genNewBombAndBall()
   
        DISPLAYSURF.fill(WHITE)
        pygame.draw.rect(DISPLAYSURF, RED, mainWindow)
        pygame.draw.rect(DISPLAYSURF, BLACK, originRectOfBalls)
        DISPLAYSURF.blit(scoreTextSurfaceObj, scoreTextRectObj)
        DISPLAYSURF.blit(collisionTextSurfaceObj, collisionTextRectObj)
        for ball in ballActiveList :
            ball.move()
            ball.speedy = ball.speedy + ball.reducey
            ball.reducey = ball.reducey + gravity*0.002
            if ball.y <= height and ball.show:
                pygame.draw.circle(DISPLAYSURF, ball.color, (int(ball.x), int(ball.y)), ball.radius, 0)
    
        i = 0
        for ball in bombs:   
            ball.move()
            ball.speedy = ball.speedy + ball.reducey
            ball.reducey = ball.reducey + gravity*0.002
 
            if ball.y <= height and ball.show:
                pygame.draw.circle(DISPLAYSURF, ball.color, (int(ball.x), int(ball.y)), ball.radius, 0)
                bombsText[i][1].center = (ball.x, ball.y)
                DISPLAYSURF.blit(bombsText[i][0], bombsText[i][1])
            i = i+1

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if isMouseDown == 0:
                    isMouseDown = 1
                    lastMouseX, lastMouseY = event.pos
                curMouseX, curMouseY = event.pos
                pygame.draw.line(DISPLAYSURF, WHITE, (lastMouseX, lastMouseY), (curMouseX, curMouseY), 3)
        
            if event.type == MOUSEMOTION:
                curMouseX, curMouseY = event.pos
                if isMouseDown:
                    pygame.draw.line(DISPLAYSURF, WHITE, (lastMouseX, lastMouseY), (curMouseX, curMouseY), 3)
        
                    for ball in ballActiveList:
                        if distPerpendicular((ball.x, ball.y), (lastMouseX, lastMouseY), (curMouseX, curMouseY)) < ball.radius :
                            if checkAngles((ball.x, ball.y), (lastMouseX, lastMouseY), (curMouseX, curMouseY)) and ball.show:
                                SCORE += 10
                                ball.show = 0

                    for ball in bombs :
                        if distPerpendicular((ball.x, ball.y), (lastMouseX, lastMouseY), (curMouseX, curMouseY)) < ball.radius:
                            if checkAngles((ball.x, ball.y), (lastMouseX, lastMouseY), (curMouseX, curMouseY)) and ball.show:
                                SCORE -= 20 
                                ball.show = 0 
                                COLLISION = COLLISION + 1
                                if COLLISION == 3:
                                    endGame()

            if event.type == MOUSEBUTTONUP:
                isMouseDown = 0

        pygame.display.update()
        fpsClock.tick(FPS)

