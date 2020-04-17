import pygame
import random
import math
import os, sys
from pygame import mixer


# Funkcja pozwalająca nadać ścieżkę systemową do zasobów
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# rozpocznij program
pygame.init()

# Pixele do odświeżenia
dirtyRects = []

# ZASOBY

font_url = resource_path("assets/Play-Regular.ttf")
player_url = resource_path("assets/tomasznowe.png")
icon_url = resource_path("assets/virus.png")
enemy_url = resource_path("assets/coronavirus.png")
enemy1_url = resource_path("assets/contamination.png")
enemy2_url = resource_path("assets/alcohol-gel.png")
spear_url = resource_path("assets/papier.png")

# Wynik
score = 0
font = pygame.font.Font(font_url, 32)
textX = 10
textY = 10


# dodaj zegar gry
clock = pygame.time.Clock()

# stworz ekran gry
screen = pygame.display.set_mode((800, 600))  # szerokość , wysokość

# nazwa gry
pygame.display.set_caption("Wirusowe urodziny")

# ikona gry
icon = pygame.image.load(icon_url)
pygame.display.set_icon(icon)

# gracz
playerImg = pygame.image.load(player_url).convert_alpha()
playerX = 368  # całość ekranu (800) / 2 - szerokość obrazka (64) / 2
playerY = 480
speedX = 0
speedY = 0
playerSpeedChange = 6

# przeciwnik
enemyImg = []
enemyX = []
enemyY = []
enemySpeedX = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(enemy_url).convert_alpha())
    enemyX.append(random.randint(1, 735))
    enemyY.append(0)
    enemySpeedX.append(random.choice([-5, -4, -3, 3, 4, 5]))

# strzal
spearImg = pygame.image.load(spear_url).convert_alpha()
spearX = -50
spearY = -50
spearSpeedY = 15
spearState = "ready"  # ready / throw

# koniec gry
over_font = pygame.font.Font(font_url, 30)
game_state = "play"  # play / over


def game_over():
    global game_state, dirtyRects, num_of_enemies, enemyY
    for j in range(num_of_enemies):
        enemyY[j] = 2000
    game_state = "over"
    over_text = over_font.render("WSZYSTKIEGO NAJLEPSZEGO Z OKAZJI URODZIN!!", True, (0, 0, 0))
    r = screen.blit(over_text, (100, 200))
    dirtyRects.append(r)


def show_score(x, y):
    scoreText = font.render("Wynik: " + str(score), True, (0, 0, 0))
    r = screen.blit(scoreText, (x, y))
    global dirtyRects
    dirtyRects.append(r)


def player(x, y):
    r = screen.blit(playerImg, (x, y))
    global dirtyRects
    dirtyRects.append(r)


def enemy(x, y, i):
    r = screen.blit(enemyImg[i], (x, y))
    global dirtyRects
    dirtyRects.append(r)


def throw_spear(x, y):
    global spearState, dirtyRects
    spearState = "throw"
    r = screen.blit(spearImg, (x + 16, y + 10))
    dirtyRects.append(r)


def is_collision(enemyX, enemyY, spearX, spearY, d):
    distance = math.sqrt((math.pow(enemyX - spearX, 2) + math.pow(enemyY - spearY, 2)))
    if distance < d:
        return True
    else:
        return False


def gen_enemy(i):
    global enemyX, enemyY, enemySpeedX
    enemyX[i] = random.randint(1, 735)
    enemyY[i] = 0
    enemySpeedX[i] = random.choice([-5, -4, -3, 3, 4, 5])


running = True

while running:
    # Tło ekranu gry
    screen.fill((236, 156, 2))  # Red Green Blue 0 --> 255

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if spearState is "ready":
                    spearY = playerY
                    spearX = playerX
                    throw_spear(spearX, spearY)



    # poprawiony ruch z klawiatury
    keys = pygame.key.get_pressed()
    speedX = 0
    speedY = 0
    if game_state == "play":
        if keys[pygame.K_LEFT]:
            speedX = -playerSpeedChange
        elif keys[pygame.K_RIGHT]:
            speedX = playerSpeedChange

        if keys[pygame.K_UP]:
            speedY = -playerSpeedChange
        elif keys[pygame.K_DOWN]:
            speedY = playerSpeedChange

    playerX += speedX
    playerY += speedY

    #  ogranicz obszar gry
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # ogranicz obszar ruchu przeciwnika
    for i in range(num_of_enemies):

        if enemyY[i] > 535:
            game_over()
            break

        if enemyX[i] <= 0:
            enemySpeedX[i] *= -1
            enemyY[i] += 64
        elif enemyX[i] >= 736:
            enemySpeedX[i] *= -1
            enemyY[i] += 64

        # kolizja?
        collision = is_collision(enemyX[i], enemyY[i], spearX, spearY, 25)
        if collision:
            spearState = "ready"
            spearY = -50
            score += 1
            gen_enemy(i)

        playerCollision = is_collision(enemyX[i], enemyY[i], playerX, playerY, 50)
        if playerCollision:
            game_over()


        enemy(enemyX[i], enemyY[i], i)

        enemyX[i] += enemySpeedX[i]

    if spearY <= -32:
        spearY = -50
        spearState = "ready"

    # strzal
    if spearState is "throw":
        throw_spear(spearX, spearY)
        spearY -= spearSpeedY

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update(dirtyRects)
    clock.tick(60)