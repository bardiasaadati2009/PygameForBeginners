import sys
import random
import time

import pygame

pygame.init()

pipEvent = pygame.USEREVENT + 1
pygame.time.set_timer(pipEvent, 1000)
birdEvent = pygame.USEREVENT
pygame.time.set_timer(birdEvent, 100)

fps = 90
width = 400
height = 710
floorx = 0
birdMove = 0
grav = 0.15
pipeList = []
game_status = True
Score = 0
activeScore = True
highScore = 0

btn = pygame.transform.scale(pygame.image.load("assets/img/flappyBirdPlayButton.png"), (120, 50))
btnRect = btn.get_rect(center=(200, 470))

bg = pygame.transform.scale(pygame.image.load('assets/img/bg2.png'), (width, height))
floorImage = pygame.transform.scale(pygame.image.load('assets/img/floor.png'), (width, 200))
pipe = pygame.image.load('assets/img/pipe_green.png')
jump = pygame.mixer.Sound('assets/sound/smb_stomp.wav')
gameOVER = pygame.mixer.Sound('assets/sound/smb_mariodie.wav')
gameOver = pygame.image.load('assets/img/message.png')
gameOverR = gameOver.get_rect(center=(200, 350))

GameOver = pygame.mixer.Sound('assets/sound/smb_mariodie.wav')
bird_up = pygame.image.load('assets/img/red_bird_up_flap.png')
bird_mid = pygame.image.load('assets/img/red_bird_mid_flap.png')
bird_down = pygame.image.load('assets/img/red_bird_down_flap.png')
font = pygame.font.Font("assets/font/Flappy.TTF", 20)

bird_list = [bird_up, bird_mid, bird_down]
bird_index = 0

bird = bird_list[bird_index]

birdRect = bird.get_rect(center=(50, 450))
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def generatePipeRect():
    rand_pos = random.randrange(350, 500)
    pipeRect = pipe.get_rect(midtop=(300, rand_pos))
    pipeRectUp = pipe.get_rect(midbottom=(300, rand_pos - 170))
    return pipeRect, pipeRectUp


def MovePipe(pipes):
    for pipeRect in pipes:
        pipeRect.centerx -= 4
        if pipeRect.right < 0:
            pipes.remove(pipeRect)

    return pipes


def drawPipes(pipes):
    for pipeRect in pipes:
        if pipeRect.bottom > 345:
            win.blit(pipe, pipeRect)
        else:
            revImage = pygame.transform.rotate(pipe, 180)
            win.blit(revImage, pipeRect)


def checkCollsion(pipes):
    for pipeRect in pipes:
        if birdRect.colliderect(pipeRect):
            gameOVER.play()
            time.sleep((2))
            return False
        if birdRect.top <= -20 or birdRect.bottom >= 570:
            gameOVER.play()
            time.sleep((2))
            return False

    return True


def birdAnime():
    newBird = bird_list[bird_index]
    newBirdRect = newBird.get_rect(center=(50, birdRect.centery))
    return newBird, newBirdRect


def displayScore(status):
    if (status == "active"):
        text = font.render(str(Score), False, (255, 255, 255))
        textRect = text.get_rect(center=(200, 100))
        win.blit(text, textRect)
    if status == "game over":
        # Score
        text = font.render("Score = " + str(Score), False, (255, 255, 255))
        textRect = text.get_rect(center=(200, 100))
        win.blit(text, textRect)
        # high Score
        text2 = font.render("High Score = " + str(highScore), False, (255, 255, 255))
        textRect2 = text2.get_rect(center=(200, 150))
        win.blit(text2, textRect2)


def updateScore():
    global Score, activeScore, highScore
    for pipeRect in pipeList:
        if 40 < pipeRect.centerx < 60 and activeScore:
            Score += 1
            activeScore = False
        if pipeRect.centerx < 40:
            activeScore = True
    if Score > highScore:
        highScore = Score


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birdMove = 0
                birdMove -= 4
                jump.play()
        pos = pygame.mouse.get_pos()
        if btnRect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                game_status = True
                birdMove = 0
                pipeList.clear()
                birdRect.center = (50, 300)
                Score = 0

        if event.type == pipEvent:
            pipeList.extend(generatePipeRect())
        if event.type == birdEvent:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, birdRect = birdAnime()

    pipeList = MovePipe(pipeList)
    floorx -= 1
    birdMove += grav
    birdRect.centery += birdMove
    win.blit(bg, (0, 0))
    win.blit(floorImage, (floorx, 570))
    win.blit(floorImage, (floorx + width, 570))
    if game_status:
        game_status = checkCollsion(pipeList)
        drawPipes(pipeList)
        win.blit(bird, birdRect)
        win.blit(floorImage, (floorx, 570))
        win.blit(floorImage, (floorx + width, 570))
        updateScore()
        displayScore("active")
    else:
        displayScore("game over")
        win.blit(gameOver, gameOverR)

        win.blit(btn, btnRect)
        jump.stop()
    if floorx <= -400:
        floorx = 0

    pygame.display.update()
    clock.tick(fps)
