import pygame
import random

pygame.init()
w = 1700
h = 900
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("фруктомания")

player_size = 200
player_speed = 12
player_x = w // 2 - player_size // 2
player_y = h - player_size - 10

circle_size = 70
banana_speed = 5
bomb_speed = 6
strawberry_speed = 8
oranges_speed = 5.5

bananas = []
bombs = []
strawberrys = []
oranges = []

score = 0
circle_timer = 2500
last_circle = pygame.time.get_ticks()

banana_image = pygame.image.load("images/banana.png")
banana_image = pygame.transform.scale(banana_image, (70, 70))

bomb_image = pygame.image.load("images/bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (80, 80))

strawberry_image = pygame.image.load("images/strawberry.png")
strawberry_image = pygame.transform.scale(strawberry_image, (70, 70))

orange_image = pygame.image.load("images/orange.png")
orange_image = pygame.transform.scale(orange_image, (70, 70))

contact_distance = 80

background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (1200, h))

intro_image = pygame.image.load("images/intro.png")
intro_image = pygame.transform.scale(intro_image, (w, h))

game_over_image = pygame.image.load("images/gameover.png")
game_over_image = pygame.transform.scale(game_over_image, (w, h))

instruction_image = pygame.image.load("images/instruction.png")
instruction_image = pygame.transform.scale(instruction_image, (600, 800))

settings_image = pygame.image.load("images/settings_button.png")
settings_image = pygame.transform.scale(settings_image, (300, 140))

play_image = pygame.image.load("images/play_button.png")
play_image = pygame.transform.scale(play_image, (300, 140))

instruction_button_image = pygame.image.load("images/instruction_button.png")
instruction_button_image = pygame.transform.scale(instruction_button_image, (300, 140))


def show_instructions():
    a = 0
    instructions_running = True
    while instructions_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                instructions_running = False

        if a < 255:
            a += 5
        else:
            a = 255

        instruction_image.set_alpha(a)

        screen.blit(instruction_image, (550, 50))
        pygame.display.flip()
        pygame.time.delay(30)

def show_intro():
    intro_running = True
    while intro_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (670 < mouse_x < 870) and (450 < mouse_y < 550):
                    show_instructions()



        screen.blit(intro_image, (0, 0))
        screen.blit(settings_image, (670, 450))
        screen.blit(instruction_button_image, (670, 550))
        screen.blit(play_image, (670, 350))
        pygame.display.flip()
        pygame.time.delay(30)


show_intro()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if k[pygame.K_RIGHT] and player_x < 1200 - player_size:
        player_x += player_speed

    current_time = pygame.time.get_ticks()
    if current_time - last_circle >= circle_timer:
        last_circle = current_time
        x = random.randint(circle_size, 1150 - circle_size)
        y = -circle_size

        fruits_type = random.choice(['orange', 'bomb', 'banana', "strawberry"])
        if fruits_type == 'orange':
            oranges.append([x, y])
        elif fruits_type == 'bomb':
            bombs.append([x, y])
        elif fruits_type == 'banana':
            bananas.append([x, y])
        else:
            strawberrys.append([x, y])

    for i in range(len(bananas) - 1, -1, -1):
        bananas[i][1] += banana_speed
        circle_x = bananas[i][0]
        circle_y = bananas[i][1]

        if (abs(player_x - circle_x) < contact_distance and
                abs(player_y - circle_y) < contact_distance):
            score += 10
            bananas.pop(i)

        elif bananas[i][1] > h + circle_size:
            bananas.pop(i)

    for i in range(len(bombs) - 1, -1, -1):
        bombs[i][1] += bomb_speed
        circle_x = bombs[i][0]
        circle_y = bombs[i][1]

        if (abs(player_x - circle_x) < contact_distance and
                abs(player_y - circle_y) < contact_distance):
            score -= 15
            bombs.pop(i)

        elif bombs[i][1] > h + circle_size:
            bombs.pop(i)

    for i in range(len(strawberrys) - 1, -1, -1):
        strawberrys[i][1] += strawberry_speed
        circle_x = strawberrys[i][0]
        circle_y = strawberrys[i][1]

        if (abs(player_x - circle_x) < contact_distance and
                abs(player_y - circle_y) < contact_distance):
            score += 30
            strawberrys.pop(i)

        elif strawberrys[i][1] > h + circle_size:
            strawberrys.pop(i)

    for i in range(len(oranges) - 1, -1, -1):
        oranges[i][1] += oranges_speed
        circle_x = oranges[i][0]
        circle_y = oranges[i][1]

        if (abs(player_x - circle_x) < contact_distance and
                abs(player_y - circle_y) < contact_distance):
            score += 20
            oranges.pop(i)

        elif oranges[i][1] > h + circle_size:
            oranges.pop(i)

    screen.fill('black')
    screen.blit(background_image, (0, 0))
    player_image = pygame.image.load("images/player.png")
    player_image = pygame.transform.scale(player_image, (140, 200))
    screen.blit(player_image, (player_x, player_y))

    for banana in bananas:
        screen.blit(banana_image, (banana[0], banana[1]))
    for bomb in bombs:
        screen.blit(bomb_image, (bomb[0], bomb[1]))
    for strawberry in strawberrys:
        screen.blit(strawberry_image, (strawberry[0], strawberry[1]))
    for orange in oranges:
        screen.blit(orange_image, (orange[0], orange[1]))

    font = pygame.font.Font(None, 55)
    text = font.render(f"Рекорд игрока: {score}", True, 'white')
    screen.blit(text, (1220, 840))
    pygame.display.flip()
    pygame.time.delay(20)
pygame.quit()