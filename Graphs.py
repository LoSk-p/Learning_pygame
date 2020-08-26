import pygame
import sys
from time import sleep
import math
import random
pygame.init()
print(pygame.display.get_init())
class Game:
    def __init__(self, screen, screenDimensions):
        self.fps = 120
        self.screenDimensions = screenDimensions
        self.frame = pygame.time.Clock()
        self.screen = screen
    def updateFrame(self):
        self.frame.tick(self.fps)
        pygame.display.flip()

class Background(Game):
    def __init__(self, screen, screenDimensions):
        Game.__init__(self, screen, screenDimensions)
        self.spaceImage = None
        self.score = 5
        self.font = pygame.font.SysFont("Arial", 25)
        self.font1 = pygame.font.SysFont("Arial", 50)
        self.scoreText = self.font.render("Lifes: " + str(self.score), True, (255, 255, 255))
        self.winText = self.font1.render("You win!", True, (255, 255, 255))
        self.gameOverText = self.font1.render("Game over", True, (255, 255, 255))
        self.pressSpaceText = self.font.render("press space to start game", True, (255, 255, 255))
        self.pressEnterText = self.font.render("press Enter", True, (255, 255, 255))
    def loadSpace(self, name):
        self.spaceImage = pygame.image.load(name).convert()
        self.spaceImage = pygame.transform.scale(self.spaceImage, self.screenDimensions)
    def blitSpace(self):
        self.screen.blit(self.spaceImage, (0,0))
        self.screen.blit(self.scoreText,
                         (800 - self.scoreText.get_width() / 2, 50 - self.scoreText.get_height() / 2))
    def text_lifes(self, lifes):
        self.scoreText = self.font.render("Lifes: " + str(lifes), True, (255, 255, 255))
    def text_win(self):
        self.screen.blit(self.winText, (450 - int(self.winText.get_width()/2), 300))
        self.screen.blit(self.pressEnterText, (450 - int(self.pressEnterText.get_width()/2), 400))
    def text_gameOver(self):
        self.screen.blit(self.pressSpaceText, (450 - int(self.pressSpaceText.get_width()/2), 400))
        self.screen.blit(self.gameOverText, (450 - int(self.gameOverText.get_width()/2), 300))
class Block(Game):
    def __init__(self, screen, screenDimensions, coords, lifes):
        Game.__init__(self, screen, screenDimensions)
        self.coords = coords
        self.lifes = lifes
        self.blockImage = None
        self.blockWidth = 50
        self.blockHeight = 20
    def makeBlock(self):
        self.blockImage = pygame.draw.rect(self.screen,
                                           (self.lifes*50, 200, 200),
                                           pygame.Rect(self.coords[0], self.coords[1],
                                                       self.blockWidth, self.blockHeight))
    def getCoords(self):
        return (self.coords[0],
                self.coords[0] + self.blockWidth,
                self.coords[1],
                self.coords[1] - self.blockHeight)
    def boom(self):
        if self.lifes > 1:
            self.lifes -= 1
            self.makeBlock()
            return False
        else:
            return True
class Platform(Game):
    def __init__(self, screen, screenDimensions):
        Game.__init__(self, screen, screenDimensions)
        self.platImage = None
        self.platWidth = 110
        self.platHeight = 20
        self.coord = [450 - self.platWidth/2, 620]
        self.startCoord = (450 - self.platWidth/2, 620)
    def startPlat(self):
        self.coord[0] = self.startCoord[0]
        self.coord[1] = self.startCoord[1]
        self.platImage = pygame.draw.rect(self.screen,
                                          (100, 200, 100),
                                          pygame.Rect(self.startCoord[0], self.startCoord[1],
                                                      self.platWidth, self.platHeight))
    def makePlat(self):
        self.platImage = pygame.draw.rect(self.screen,
                                          (100,200,100),
                                          pygame.Rect(self.coord[0], self.coord[1],
                                                      self.platWidth, self.platHeight))
    def movePlat(self, direction, speed):
        if direction == "Right":
            self.coord[0] += speed
            self.platImage = pygame.draw.rect(self.screen,
                                              (100, 200, 100),
                                              pygame.Rect(self.coord[0], self.coord[1],
                                                          self.platWidth, self.platHeight))
        elif direction == "Left":
            self.coord[0] -= speed
            self.platImage = pygame.draw.rect(self.screen,
                                              (100, 200, 100),
                                              pygame.Rect(self.coord[0], self.coord[1],
                                                          self.platWidth, self.platHeight))
    def getCoords(self):
        return (self.coord[0],
                self.coord[0] + self.platWidth,
                self.coord[1],
                self.coord[1] + self.platHeight)
class Ball(Game):
    def __init__(self, screen, screenDimensions):
        Game.__init__(self, screen, screenDimensions)
        self.ballImage = None
        self.radius = 8
        self.centreCoord = [450, 615 - self.radius]
        self.startCoord = (450, 615 - self.radius)
        self.leftCoord = self.centreCoord[0] - self.radius
        self.rightCoord = self.centreCoord[0] + self.radius
        self.highCoord = self.centreCoord[1] - self. radius
        self.lowCoord = self.centreCoord[1] + self.radius
        self.Xcentre = self.centreCoord[0]
        self.Ycentre = self.centreCoord[1]
    def makeBall(self):
        self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100),self.centreCoord, self.radius)
    def startBall(self):
        self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100), self.startCoord, self.radius)
        self.centreCoord[0] = self.startCoord[0]
        self.centreCoord[1] = self.startCoord[1]
        self.Xcentre = self.centreCoord[0]
        self.Ycentre = self.centreCoord[1]
    def moveBall(self, direction, speed):
        if direction == "Left":
            self.centreCoord[0] -= speed
            self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100), self.centreCoord, self.radius)
        elif direction == "Right":
            self.centreCoord[0] += speed
            self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100), self.centreCoord, self.radius)
        self.Xcentre = self.centreCoord[0]
    def flyBall(self, angle, direction, speed):
        if direction == 1:
            #print(self.centreCoord)
            #print(angle)
            self.Xcentre += math.cos(angle*math.pi/180)*speed
            self.Ycentre -= math.sin(angle*math.pi/180)*speed
            self.centreCoord[0] = int(self.Xcentre)
            self.centreCoord[1] = int(self.Ycentre)
            #print(self.centreCoord)
            self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100),
                                                self.centreCoord,
                                                self.radius)
        elif direction == -1:
            self.Xcentre += math.cos(angle * math.pi / 180) * speed
            self.Ycentre += math.sin(angle * math.pi / 180) * speed
            self.centreCoord[0] = int(self.Xcentre)
            self.centreCoord[1] = int(self.Ycentre)
            self.ballImage = pygame.draw.circle(self.screen, (200, 200, 100),
                                                self.centreCoord,
                                                self.radius)
        #print(self.Ycentre)
    def checkBoom(self, rect):
        if self.ballImage.colliderect(rect):
            if rect.left <= self.ballImage.center[0] and self.ballImage.center[0] <= rect.right:
                if self.ballImage.top <= rect.bottom and self.ballImage.bottom >= rect.bottom:
                    return "Bottom"
                elif self.ballImage.bottom >= rect.top and self.ballImage.top <= rect.top:
                    return "Top"
            elif rect.top <= self.ballImage.center[1] and self.ballImage.center[1] <= rect.bottom:
                if self.ballImage.left <= rect.right and self.ballImage.right >= rect.right:
                    return "Left"
                elif self.ballImage.left <= rect.left and self.ballImage.right >= rect.left:
                    return "Right"
            elif self.ballImage.center[0] >= rect.right:
                if self.ballImage.center[1] <= rect.top:
                    return "RightTop"
                else:
                    return "RightBottom"
            else:
                if self.ballImage.center[1] <= rect.top:
                    return "LeftTop"
                else:
                    return "LeftBottom"
        else:
            return "No"


def updateFrameImages():
    global background, platform, blocks, newBall
    background.blitSpace()
    blitBlocks(blocks)
    #platform.makePlat()
    if newBall == True:
        platform.startPlat()
        ball.startBall()
        #print("New ball")
        newBall = False
    else:
        ball.makeBall()
        platform.makePlat()
    if win == True:
        background.text_win()
    if gameOver == True:
        background.text_gameOver()
    if beforeStart == True:
        screen.blit(background.pressSpaceText, (450 - int(background.pressSpaceText.get_width() / 2), 400))

def blitBlocks(blocks):
    for row in blocks:
        for block in row:
            block.makeBlock()
def blocksMap(map):
    blocks = [[]]
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != 0:
                blocks[i].append(Block(screen, screenDim, (55 * j + 5, 25 * i + 5), map[i][j]))
        blocks.append([])
    return blocks

width = 900
height = 700
screenDim = (width, height)
screen = pygame.display.set_mode(screenDim)
pygame.display.set_caption("My First Game")
game = Game(screen, screenDim)
background = Background(screen, screenDim)
background.loadSpace("space.jpg")
background.blitSpace()
platform = Platform(screen, screenDim)
platform.makePlat()
ball = Ball(screen, screenDim)
ball.makeBall()
map = [[0, 0, 4, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 5, 5, 5, 5, 4, 5, 5, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 3, 3, 3, 5, 5, 5, 5, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 4, 4, 4, 5, 5, 5, 5, 0, 0, 0],
       [0, 0, 3, 3, 3, 3, 3, 2, 3, 3, 3, 5, 5, 5, 0, 0]]
blocks = blocksMap(map)
blitBlocks(blocks)
screen.blit(background.pressSpaceText, (450 - int(background.pressSpaceText.get_width()/2), 400))
#pygame.draw.circle(screen, (200, 100, 100), (100,100), 20)
#pygame.draw.rect(screen, (0, 250, 100), pygame.Rect(10, 0, 20, 30))

#def blitAll(showFoot = False):
#    global
startBlocks = []
for row in blocks:
    startBlocks.append(row.copy())
platSpeed = 3
ballSpeed = 3
finished = False
ballFly = False
newBall = False
win = False
gameOver = False
beforeStart = True
lifesNomber = 5
lifes = 5
while finished == False:
    #processing all events
    for event in pygame.event.get():
        #do appropriate things with events
        if event.type == pygame.QUIT:
            finished = True
            pygame.quit()
            sys.exit()
    pressedKeys = pygame.key.get_pressed()
    #print(ball.ballImage.center)
    platCoords = platform.getCoords()
    #print(ball.checkBoom(platform.platImage))
    if pressedKeys[pygame.K_LEFT] == 1:
        if platCoords[0] > 5:
            platform.movePlat("Left", platSpeed)
            if ballFly == False:
                ball.moveBall("Left", platSpeed)
    elif pressedKeys[pygame.K_RIGHT] == 1:
        if platCoords[1] < 895:
            platform.movePlat("Right", platSpeed)
            if ballFly == False:
                ball.moveBall("Right", platSpeed)
    elif pressedKeys[pygame.K_SPACE] == 1:                  # Начало игры
        beforeStart = False
        gameOver = False
        if ballFly == False:
            print("Fly")
            angle = (900 - platform.platImage.center[0])*180/900
            print((900 - platform.platImage.center[0])*180/900)
            direction = 1
            ballFly = True
            ball.flyBall(angle, direction, ballSpeed)
    elif pressedKeys[pygame.K_RETURN] == 1:
        print("enter")
        win = False
        blocks = blocksMap(map)
        lifes = 5
        background.text_lifes(lifes)
        blitBlocks(blocks)


    boom = 0
    for row in blocks:                                  # Столкновение с блоками (вычисление места)
        for block in row:
            if ball.checkBoom(block.blockImage) != "No":
                boom = ball.checkBoom(block.blockImage)
                if block.boom():
                    row.remove(block)

    #print(boom)
    if ball.checkBoom(platform.platImage) != "No":      # Столкновение с тележкой
        platBoom = ball.checkBoom(platform.platImage)
        if platBoom == "Top":
            direction = 1
            angle = 180 - (ball.ballImage.center[0] - platform.platImage.left + 20)*180/150

    if ball.ballImage.left <= 0:                       # Столкновение с левой стеной
        ball.moveBall("Right", ballSpeed*2)
        print("left")
        print("angle ", angle)
        print("direction ", direction)
        if direction == 1:
            if angle >= 90:
                angle -= 180 - 2*(180 - angle)
        else:
            if angle >= 90:
                angle -= 180 - 2*(180 - angle)
    if ball.ballImage.right >= width:                  # Столкновение с правой стеной
        print("right")
        print("angle", angle)
        print("direction ", direction)
        ball.moveBall("Left", ballSpeed*2)
        if direction == 1:
            if angle <= 90:
                angle += 180 - 2*angle
        else:
            if angle <= 90:
                angle += 180 - 2*angle
    if ball.ballImage.top <= 0:                   # Столкновение с потолком
        direction *= -1
    if ball.ballImage.bottom >= height:            # Столкновение с полом
        lifes -= 1
        newBall = True
        ballFly = False
        if lifes == 0:                              # Конец игры
            blocks = blocksMap(map)
            gameOver = True
            background.text_gameOver()
            lifes = 5
        background.text_lifes(lifes)
    k = 0
    for row in blocks:
        for block in row:
            if block != 0:
                k += 1
    #print(blocks)
    if k == 0:
        win = True
        background.text_win()
        newBall = True
        ballFly = False
    if boom == "Bottom":                            # Столкновение с блоками (движение)
        print("BOOM")
        direction = -1
    elif boom == "Top":
        direction = 1
    elif boom == "Left":
        if direction == 1:
            if angle >= 90:
                angle -= 180 - 2*(180 - angle)
        else:
            if angle >= 90:
                angle -= 180 - 2*(180 - angle)
    elif boom == "Right":
        if direction == 1:
            if angle <= 90:
                angle += 180 - 2 * angle
        else:
            if angle <= 90:
                angle += 180 - 2 * angle
    elif boom == "RightTop":
        direction = 1
        angle = random.randint(20, 70)
    elif boom == "RightBottom":
        direction = -1
        angle = random.randint(20, 70)
    elif boom == "LeftTop":
        direction = 1
        angle = random.randint(110, 160)
    elif boom == "LeftBottom":
        direction = -1
        angle = random.randint(110, 160)

    #print(ball.ballImage.left, ball.bahttps://losst.ru/wp-content/uploads/2016/07/update6.pngllImage.right, ball.ballImage.top)
    if ballFly == True:
        ball.flyBall(angle, direction, ballSpeed)
    #blitAll()
    updateFrameImages()
    game.updateFrame()
#pygame.quit()