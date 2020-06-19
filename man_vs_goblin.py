# Initialize the pygame libriry
import pygame
from pygame import mixer
import math
import os, os.path
pygame.init()

clock = pygame.time.Clock()

# Background music
mixer.music.load(os.path.join('Sound', 'background_music.wav'))
mixer.music.play(-1)

xCoordinate = 0
yCoordinate = 330
playerWidth = 64
playerHeight = 64
velocity = 6
isJump = False
jumpCount = 10
left = False
right = True
walkCount = 0
screenLength = 800
screenBreadth = 600
bulletPos = 0
shoot = False
direction = True
enemy = False
enemyWalk = 0
enemyRelease = False
enemyX = 0
sign = 1
point = 0
man = 0
gameOver = False
call = 5
font = pygame.font.Font('freesansbold.ttf', 25)

manHealth = enemyHealth = 100

screen = pygame.display.set_mode((screenLength, screenBreadth))
pygame.display.set_caption('Fighter Game')



enemyRight = [pygame.image.load(os.path.join('Images', 'enemy', 'ER1.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER2.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER3.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER4.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER5.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER6.png')), pygame.image.load(os.path.join('Images', 'enemy', 'ER7.png'))]
enemyLeft = [pygame.image.load(os.path.join('Images', 'enemy', 'EL1.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL2.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL3.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL4.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL5.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL6.png')), pygame.image.load(os.path.join('Images', 'enemy', 'EL7.png'))]
walkRight = [pygame.image.load(os.path.join('Images', 'player', 'R0.png')), pygame.image.load(os.path.join('Images', 'player', 'R1.png')), pygame.image.load(os.path.join('Images', 'player', 'R2.png')), pygame.image.load(os.path.join('Images', 'player', 'R3.png')), pygame.image.load(os.path.join('Images', 'player', 'R4.png')), pygame.image.load(os.path.join('Images', 'player', 'R5.png')), pygame.image.load(os.path.join('Images', 'player', 'R6.png')), pygame.image.load(os.path.join('Images', 'player', 'R7.png')), pygame.image.load(os.path.join('Images', 'player', 'R8.png')), pygame.image.load(os.path.join('Images', 'player', 'R9.png')), pygame.image.load(os.path.join('Images', 'player', 'R10.png'))]
walkLeft = [pygame.image.load(os.path.join('Images', 'player', 'L0.png')), pygame.image.load(os.path.join('Images', 'player', 'L1.png')), pygame.image.load(os.path.join('Images', 'player', 'L2.png')), pygame.image.load(os.path.join('Images', 'player', 'L3.png')), pygame.image.load(os.path.join('Images', 'player', 'L4.png')), pygame.image.load(os.path.join('Images', 'player', 'L5.png')), pygame.image.load(os.path.join('Images', 'player', 'L6.png')), pygame.image.load(os.path.join('Images', 'player', 'L7.png')), pygame.image.load(os.path.join('Images', 'player', 'L8.png')), pygame.image.load(os.path.join('Images', 'player', 'L9.png')), pygame.image.load(os.path.join('Images', 'player', 'L10.png'))]
background = pygame.image.load(os.path.join('Images', 'background', 'background.png'))
arrowR = pygame.image.load(os.path.join('Images', 'arrow', 'AR.png')) 
arrowL = pygame.image.load(os.path.join('Images', 'arrow', 'AL.png'))

def arrowShoot(direction):

    global bulletPos
    if bulletPos < screenLength and bulletPos > 0: 
        if direction == False:
            var = -1
            arrow = arrowL
        if direction == True:
            var = 1
            arrow = arrowR
        bulletPos += 35 * var
        screen.blit(arrow, (bulletPos, 350)) 

    else:
        shoot = False
        return
    

def enemy(sign):
    global enemyWalk 
    global enemyX
    enemyWalk += 1
    enemyX = enemyX - (5 * sign)
    if enemyWalk == 21:
        attackSound = mixer.Sound(os.path.join('Sound', 'enemy_attack.wav'))
        attackSound.play()
        enemyWalk = 0
    if sign == 1:
        screen.blit(enemyLeft[enemyWalk // 3], (enemyX, 270))
    else:
        screen.blit(enemyRight[enemyWalk // 3], (enemyX, 270))


def isArrowCollision(bulletPos, enemyX):
    # print('bullet ' + str(bulletPos))
    # print('enemy ' + str(enemyX))
    arrowDistance = int(math.sqrt((math.pow(bulletPos - enemyX, 2)) + (math.pow(350 - 270, 2))))
    # print('arrowDistance ' + str(arrowDistance))
    if arrowDistance < 100 and arrowDistance > 90:
        return True


def isEnemyCollision(xCoordinate, enemyX):
    enemyDistance = int(math.sqrt((math.pow(enemyX - xCoordinate, 2)) + (math.pow(350 - 270, 2))))
    # print(enemyDistance)
    # print(xCoordinate)
    if enemyDistance > 90 and enemyDistance <= 92 and yCoordinate == 330:
        return True
    
def scoreDisplay(manHealth, enemyHealth):
    if manHealth < 0:
        manHealth = 0
    elif enemyHealth < 0:
        enemyHealth = 0
    manScore = font.render('PLAYER health: ' + str(manHealth), True, (255, 0, 0))
    enemyScore = font.render('ENEMY health: ' + str(enemyHealth), True, (0, 0, 0))
    screen.blit(manScore, (10, 30))
    screen.blit(enemyScore, (550, 30))


def gameOverText(call):
    # call == 1 then enemy health is zero
    # call == 0 then man's health is zero
    if call == 1:
        fontNew = pygame.font.Font('freesansbold.ttf', 50)
        over = fontNew.render('GAME OVER', True, (0, 0, 0))
        screen.blit(over, (240, 130))
        fontMan = pygame.font.Font('freesansbold.ttf', 30)
        manWins = fontMan.render('YOU WON', True, (0, 0, 0))
        screen.blit(manWins, (335, 200))
        screen.blit(walkRight[0], (335, yCoordinate))
    elif call == 0:
        fontNew = pygame.font.Font('freesansbold.ttf', 50)
        over = fontNew.render('GAME OVER', True, (0, 0, 0))
        screen.blit(over, (240, 130))
        fontEnemy = pygame.font.Font('freesansbold.ttf', 30)
        enemyWins = fontEnemy.render('ENEMY WINS', True, (0, 0, 0))   
        screen.blit(enemyWins, (290, 200))
        screen.blit(enemyLeft[0], (290, 270))

# Run until the user presses the close button or Escape key
running = True
while running:

    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    # Check if the user has pressed the quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    if not (gameOver):
        if enemyWalk + 1 >= 30:
            enemyWalk = 0
            
        if walkCount + 1 >= 30:
            walkCount = 0

        if left:
            screen.blit(walkLeft[walkCount // 3], (xCoordinate, yCoordinate))
            walkCount += 1
        elif right:
            screen.blit(walkRight[walkCount // 3], (xCoordinate, yCoordinate))
            walkCount += 1
        else:
            if left:
                screen.blit(walkLeft[0], (xCoordinate, yCoordinate))
            else:
                screen.blit(walkRight[0], (xCoordinate, yCoordinate))
    
        # Checks if arrow keys are pressed and moves in that direction
    
    
        if keys[pygame.K_LSHIFT]:
            arrowSound = mixer.Sound(os.path.join('Sound', 'arrow_shoot.wav'))
            arrowSound.play()
            bulletPos = xCoordinate
            if right:
                direction = True
            else:
                direction = False
            shoot = True
        if shoot:
            arrowShoot(direction)

        if keys[pygame.K_UP]:
            enemyRelease = True
            enemyX = 700
            pygame.mixer.music.stop()
            bossMusic = mixer.Sound(os.path.join('Sound', 'boss_music.wav'))
            bossMusic.play()
        if enemyRelease:
            if enemyX > 700:
                sign = 1
            elif enemyX < 0:
                sign = -1
            enemy(sign)

    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_SPACE]:
        isJump = True
        jumpSound = mixer.Sound(os.path.join('Sound', 'jump.wav'))
        jumpSound.play()
    if keys[pygame.K_LEFT] and xCoordinate > 0:
        xCoordinate -= velocity
        left = True
        right = False
        # direction = False
    elif keys[pygame.K_RIGHT] and xCoordinate < screenLength - playerWidth:
        xCoordinate += velocity
        left = False
        right = True
        # direction = True
    else:
        # left = False
        # right = False
        walkCount = 0

    arrowCollision = isArrowCollision(bulletPos, enemyX)
    if arrowCollision:
        enemyHealth -= 5
        bulletPos = 800
        # print(point)
        if enemyHealth == 0:
            call = 1
            gameOver = True


    enemyCollision = isEnemyCollision(xCoordinate, enemyX)
    if enemyCollision:
        manHealth -= 20
        if manHealth == 0:
            call = 0
            gameOver = True

    
    # if manHealth > 0 and enemyHealth > 0:
    scoreDisplay(manHealth, enemyHealth)

    gameOverText(call)
    
    if isJump:

        if jumpCount >= -10:
            pos = 1
            if jumpCount < 0:
                pos = -1 
            yCoordinate -= int((jumpCount ** 2) * 0.5 * pos)
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    

    pygame.display.update()


pygame.quit()
