import pygame
from pygame import mixer
import random
import math

# initialize pygame
pygame.init()

# create the screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player_ship.png')
playerX = 368
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 2

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 776))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(1)
    enemyY_change.append(0)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('missile.png')
bulletX = 0
bulletY = 480
bulletY_change = -8
bullet_state = "ready"

# Players current score (will increment +1 for every regular enemy killed)
score = 0
scoretick = 4
enemymultiplier = 1
flag = False

font = pygame.font.Font('freesansbold.ttf', 16)
scoreX = 10
scoreY = 10

enemynumX = 10
enemynumY = 30

over_font = pygame.font.Font('freesansbold.ttf', 64)


# Function to print text on the screen. Flexible for multiple uses
def show_text(x, y, text, string, color):
    score_value = font.render(string + str(text), True, color)
    screen.blit(score_value, (x, y))


# Function to print game over text on the screen
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


# Function to print winning text on the screen
def winner_text():
    win_text = over_font.render("YOU WIN", True, (0, 255, 0))
    screen.blit(win_text, (265, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 24, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27 and bullet_state == "fire":
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Function to increase amount of enemies whenever score hits a factor of 2
    if (scoretick == score) or (scoretick % 10 == 0 and scoretick >= 100) or (scoretick % 8 == 0 and scoretick >= 250) or (scoretick % 6 == 0 and scoretick >= 375):
        num_of_enemies += 1
        scoretick += 4
        flag = True

    # if keystroke is pressed, check whether it is right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        # if either key is released, also check to make sure the key released is the same as the key causing the movement. If check passes, stop movement.
        if (event.key == pygame.K_LEFT and playerX_change - 5) or (event.key == pygame.K_RIGHT and playerX_change == 5):
            playerX_change = 0

    playerX += playerX_change

    # enemy movement clauses
    for i in range(num_of_enemies):

        if flag:
            enemyImg.append(pygame.image.load('ufo.png'))
            enemyX.append(random.randint(0, 776))
            enemyY.append(random.randint(50, 100))
            enemyX_change.append(1)
            enemyY_change.append(0)
            flag = False
            enemy_Sound = mixer.Sound('enemyspawn.wav')
            enemy_Sound.play()
            print("Enemy Created!")

        # Game Over Clause
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Game Victory Clause
        if score >= 512:
            for j in range(num_of_enemies):
                enemyY[j] = -2000
            winner_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyY[i] += 26
            enemyX_change[i] = 1
        elif enemyX[i] >= 766:
            enemyX[i] = 766
            enemyY[i] += 26
            enemyX_change[i] = -1

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 776)
            enemyY[i] = random.randint(50, 100)

        # display the enemy
        enemy(enemyX[i], enemyY[i], i)

        # enemy wall collision clause
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        enemyY_change[i] = 0

    # player movement clauses
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # bullet movement clauses
    if bulletY <= -16:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    # display the player
    player(playerX, playerY)

    # display the score and enemy count
    show_text(scoreX, scoreY, score, "Score: ", (0, 255, 0))
    show_text(enemynumX, enemynumY, num_of_enemies, "Enemies: ", (255, 0, 0))

    # update the display
    pygame.display.update()