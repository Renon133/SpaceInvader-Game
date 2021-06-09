import pygame
import random, math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Define Variables
WIDTH = 800
HEIGHT = 600
PosX = 370
PosY = 480
MoveX = 0
MoveY = 0
Speed = 10
enemySpeedX = 8
enemyMoveY = 40
FrameRate = 45
BoundaryLeft = 0
BoundaryRight = 736
BoundaryTop = 0
BoundaryBottom = 536

# Score
Score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#GAme Over
endFont = pygame.font.Font('freesansbold.ttf', 64)

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initializing Clock
clock = pygame.time.Clock()

# Design of the screen and objects

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("background.png")
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
arcadeShip = pygame.image.load("space-invaders.png")
enemyImg = pygame.image.load("alien.png")
bullet = pygame.image.load("bullet.png")

# Utility Functions

def game_over():
    over_text = endFont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render("Score : "+ str(Score), True, (255,255,255))
    screen.blit(score, (x, y))

# Define Classes

class Player:
    playerX = None
    playerY = None
    playerImg = None

    def __init__(self, X, Y, image):
        self.playerX = X
        self.playerY = Y
        self.playerImg = image

    def show(self):
        screen.blit(self.playerImg, (self.playerX, self.playerY))

    def update(self, inputX, inputY):
        newX = self.playerX + inputX
        newY = self.playerY + inputY

        if newX > BoundaryLeft and newX < BoundaryRight:
            self.playerX = newX
        if newY > BoundaryTop and newY < BoundaryBottom:
            self.playerY = newY


class Enemy:
    enemyX=None
    enemyY = None
    enemyImg = None

    def __init__(self, X, Y, img):
        self.enemyY = Y
        self.enemyX = X
        self.enemyImg = img

    def show(self):
        screen.blit(self.enemyImg, (self.enemyX, self.enemyY))

    def update(self):
        global enemySpeedX
        self.enemyX += enemySpeedX
        if self.enemyX <= 0:
            enemySpeedX = 8
            self.enemyY += 40
        elif self.enemyX >= 736:
            enemySpeedX = -8
            self.enemyY += 40

# We will create objects of bullet in while loop

class Bullet:
    bulletX = 0
    bulletY = 0
    bulletImg = None

    def __init__(self, img):
        self.bulletImg = img

    def show(self):
        screen.blit(self.bulletImg, (self.bulletX, self.bulletY))

    def fire(self, playerX, playerY):
        self.bulletX = playerX + 16
        self.bulletY = playerY - 32

    def update(self):
        self.bulletY -= 10


def detectCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    return True if distance < 35 else False

# Defining Objects
playerA = Player(PosX, PosY, arcadeShip)
enemies = list()
numEnemies = 6
enemyA = Enemy(random.randint(0,735), random.randint(0,250), enemyImg)
for i in range(numEnemies):
    enemies.append(Enemy(random.randint(0,735), random.randint(0,250), enemyImg))
numEnemies = 6
bulletsFired = list()
bulletCount = 0
running = True

while running:
    # To clean screen
    clock.tick(FrameRate)
    screen.blit(background, (0,0))
    # Creating enemies
    # for i in range(numEnemies):
    #     enemies.append(Enemy(random.randint(0,735), random.randint(0,250), enemyImg) )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                MoveX = -Speed
            if event.key == pygame.K_RIGHT:
                MoveX = Speed
            if event.key == pygame.K_UP:
                MoveY = -Speed
            if event.key == pygame.K_DOWN:
                MoveY = Speed
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound('laser.wav')
                bulletSound.play()
                bulletsFired.append(Bullet(bullet))
                bulletsFired[-1].fire(playerA.playerX, playerA.playerY)
                bulletCount += 1

        elif event.type == pygame.KEYUP:
            MoveY = 0
            MoveX = 0

    # Updating movement of player and enemies
    playerA.update(MoveX, MoveY)
    idx = 0
    collision = bool

    n = len(bulletsFired)
    print(len(bulletsFired))
    i = 0
    while i < n:
        bulletsFired[i].update()
        for idx in range(numEnemies):
            collision = detectCollision(enemies[idx].enemyX, enemies[idx].enemyY, bulletsFired[i].bulletX, bulletsFired[i].bulletY)
            if collision:
                n -= 1
                explosionSound=mixer.Sound('explosion.wav')
                explosionSound.play()
                print(" Bullets: ", len(bulletsFired))
                Score += 10
                print(Score)
                enemies[idx] = Enemy(random.randint(0,800)-32, random.randint(0,200), enemyImg)
        i += 1

    # Show the image on screen
    playerA.show()
    for i in range(numEnemies):
        if enemies[i].enemyY > 600:
            for j in range(numEnemies):
                enemies[j].enemyY = 2000
                enemies[j].show()
            game_over()
            break
        enemies[i].show()
        enemies[i].update()

    for i in range(len(bulletsFired)):
        bulletsFired[i].show()
        bulletsFired[i].update()

    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
