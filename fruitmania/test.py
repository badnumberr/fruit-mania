import pygame
import random

pygame.init()
w = 1600
h = 1000
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

bananas = []
bombs = []
strawberrys = []

score = 0
circle_timer = 2500
last_circle = pygame.time.get_ticks()

yellow_image = pygame.image.load("banana.png")
yellow_image = pygame.transform.scale(yellow_image, (70, 70))

red_image = pygame.image.load("bomb.png")
red_image = pygame.transform.scale(red_image, (80, 80))

blue_image = pygame.image.load("strawberry.png")
blue_image = pygame.transform.scale(blue_image, (70, 70))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if k[pygame.K_RIGHT] and player_x < 1100 - player_size:
        player_x += player_speed

    current_time = pygame.time.get_ticks()
    if current_time - last_circle >= circle_timer:
        last_circle = current_time
        x = random.randint(circle_size, 1100 - circle_size)  # Ограничение для фруктов по оси X
        y = -circle_size

        circle_type = random.choice(['yellow', 'red', 'blue'])
        if circle_type == 'yellow':
            bananas.append([x, y])
        elif circle_type == 'red':
            bombs.append([x, y])
        else:
            strawberrys.append([x, y])

    for i in range(len(bananas) - 1, -1, -1):
        bananas[i][1] += banana_speed
        circle_x = bananas[i][0]
        circle_y = bananas[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score += 10
            bananas.pop(i)

        elif circle_x < 0 or circle_x > w - circle_size:
            bananas.pop(i)

        elif bananas[i][1] > h + circle_size:
            bananas.pop(i)

    for i in range(len(bombs) - 1, -1, -1):
        bombs[i][1] += bomb_speed
        circle_x = bombs[i][0]
        circle_y = bombs[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score -= 15
            bombs.pop(i)

        elif circle_x < 0 or circle_x > w - circle_size:
            bombs.pop(i)

        elif bombs[i][1] > h + circle_size:
            bombs.pop(i)

    for i in range(len(strawberrys) - 1, -1, -1):
        strawberrys[i][1] += strawberry_speed
        circle_x = strawberrys[i][0]
        circle_y = strawberrys[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score += 30
            strawberrys.pop(i)

        elif circle_x < 0 or circle_x > w - circle_size:
            strawberrys.pop(i)

        elif strawberrys[i][1] > h + circle_size:
            strawberrys.pop(i)

    screen.fill('black')
    player_image = pygame.image.load("player.png")
    player_image = pygame.transform.scale(player_image, (140, 200))
    screen.blit(player_image, (player_x, player_y))

    for banana in bananas:
        screen.blit(yellow_image, (banana[0], banana[1]))
    for circle in bombs:
        screen.blit(red_image, (circle[0], circle[1]))
    for circle in strawberrys:
        screen.blit(blue_image, (circle[0], circle[1]))

    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}", True, 'white')
    screen.blit(text, (10, 10))
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
