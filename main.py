import math
import random
import pygame
# mixer class helps us handle all kinds of music inside of our project 
from pygame import mixer


"""
Name: Yanbin Zuo
Date: 8/25/2021
NOTE: THIS PROJECT IS LEARNED FROM YOUTUBE VIDEO https://youtu.be/FfWpgLFMI7w
THE ORIGINAL CREATER IS FROM freeCodeCamp.org
"""
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (118, 128, 128)
TURQUOISE = (64, 224, 208)

# first, need to intialize the pygame
# REMEMBER: MUST HAVE THIS LINE, AND IT HAS TO BE FIRST
pygame.init()

# create teh screen with width(left to right) 800, and high(up to down) 600
screen = pygame.display.set_mode((800, 600))


# Title and Icon
# it has a default title in the upper left corner of the window, which
# named "pygame window" and default icon
# we change to our own title and icon
# www.flaticon.com --> find image (spaceship)
pygame.display.set_caption("Space Invaders")
# icon is 32px
icon = pygame.image.load('Images/ufo.png')
pygame.display.set_icon(icon)


# create background
# background image: pixabay.com
bgImg = pygame.image.load('Images/background.jpg')
def background():
    screen.blit(bgImg, (0,0))
# background music
mixer.music.load('Sounds/background.wav')
# if don't add anything in play(), it will only play once and stop
# add -1 means play on loop
mixer.music.play(-1)


# create player image (arcade space) 64px
playerImg = pygame.image.load('Images/space-invaders.png')
# play image applear index (x, y with the upper left of the image)
playerX = 370
playerY = 480
playerX_change_value = 0.5
playerX_change = 0
def player(x, y):
    # blit means to draw
    screen.blit(playerImg, (x, y))


# create bullet: image 32px
bulletImg = pygame.image.load('Images/bullet.png')
# will set x index to player x index
bulletX = -1
# a little bit below the player
bulletY = 490
bulletY_change = 1
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bullet_state = 'ready'
def fire_bullet(x, y):
    # player image is 32px, we put bullet in center of player, so x + 32/2
    screen.blit(bulletImg, (x + 16, y))


# create enemy: image 64px
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 60
enemy_number = 6
for i in range(enemy_number):
    enemyImg.append(pygame.image.load('Images/enemy.png'))
    enemyX.append(10 + i*100)
    enemyY.append(120)
    enemyX_change.append(0.2)
def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
    if distance < 27:
        return True
    else:
        return False


# score
score_value = 0
scoreX = 10
scoreY = 10
# this is one free font inside of pygame, 32 is size  
# go to https://www.dafont.com/ to download and upzip other free font files and
# paste the ttf file inside this project folder to use other fonts  
score_font = pygame.font.Font('Sushi Delivery.ttf', 32)
# score_value is integer, convert it to string 
def score(x, y):
    score_render = score_font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score_render, (x, y))

# game over text
game_over_font = pygame.font.Font('Sushi Delivery.ttf', 64)
def gameover():
    game_over_render = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_render, (200,250))

# Game Loop
# without loop, the screen displayed, and then the program end, then the
# screen will disappear quickly
running = True
while running:
    # everything that you want to be persistent inside the game window (appears
    # continuously, it can be image or text), it has to go inside the while loop

    # change the background color
    # make sure every other draws will below this method, otherwise, they will 
    # covered by this background color
    # (...) is a tuple
    # give RGB values (RED, GREEN, BLUE)
    # google color to rgb
    # screen.fill(CYAN) --> this also work, default is black also    
    screen.fill((0, 255, 255))

    # some background image might be very big(e.g. 1000KB), the while loop need time
    # to load the image, cause the player and enemy run slow
    background()

    # go through the list of events that are happening inside the game window
    # (any kind of input control) one by one to check which event is happening
    # events could include any keystrock that is pressed on a keyboard, and
    # mouse click...and so on
    for event in pygame.event.get():
        # the right up corner cross button is pygame.QUIT event
        # if click cross button, end the loop, which will end the program
        if event.type == pygame.QUIT:
            running = False
        
        # check if a keystroke is pressed
        # 如果一直按着按键不松开，只会相应一次
        if event.type == pygame.KEYDOWN:
            # check whether it is right or left            
            if event.key == pygame.K_LEFT:
                # print('Left arrow is pressed')    --------------> PRACTICE CODE
                playerX_change = -1 * playerX_change_value
            if event.key == pygame.K_RIGHT:
                # print('Right arrow is pressed')   --------------> PRACTICE CODE
                playerX_change = playerX_change_value
            # check for bullet fire
            if event.key == pygame.K_SPACE:
                # only ready to fire, then change state, otherwise, don't update
                if bullet_state == 'ready':
                    # add bullet sound. 
                    # if sound is very short, use sound instead of music
                    bullet_sound = mixer.Sound('Sounds/laser.wav')
                    bullet_sound.play()
                    # change bullet state
                    bullet_state = 'fire'
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
        # check if a keystroke is released
        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #     # print('Keystroke has been released')  ---------> PRACTICE CODE
            # check condition that both left key and right key are pressed
            if ((event.key == pygame.K_LEFT and playerX_change == -1 * playerX_change_value) or  
                    (event.key == pygame.K_RIGHT and playerX_change == playerX_change_value)):
                playerX_change = 0 

    # player
    # show player image and its position
    playerX += playerX_change
    # add boundary
    # without restriction, ship will go beyond the window
    if playerX <= 0:
        playerX = 0
    # since winwon is 800, and image is 64px, so right limit is :800 - 64 = 736
    elif playerX >= 736:
        playerX = 736
    player(playerX, playerY)

    # bullet
    if bulletY <= 0:
        bulletY = 490
        bullet_state = 'ready'
    # only if the bullet state is 'fire', then show bullet image and move
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # enemy
    for i in range(enemy_number):
        # check game over
        # 60*7=420 60*8 = 480
        if enemyY[i] >= 400:
            # if game over, remove all enemies
            for j in range(enemy_number):
                enemyY[j] = 1000
            gameover()
            break

        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change
        enemy(i, enemyX[i], enemyY[i])

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # add colission sound
            collision_sound = mixer.Sound('Sounds/explosion.wav')
            collision_sound.play()
            # update everything
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] -= enemyY_change
            bullet_state = 'ready'
            bulletY = 490
    
    # score
    score(scoreX, scoreY)
    
    # if add anything inside window, need update
    # REMEMBER: MUST HAVE THIS LINE, AND IT IN THE BOTTON OF THE LOOP
    pygame.display.update()
