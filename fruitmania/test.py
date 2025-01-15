import pygame
import random

pygame.init()
w = 800
h = 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("фруктомания")


player_size = 100
player_speed = 10
player_x = w // 2 - player_size // 2
player_y = h - player_size - 10

circle_size = 20
yellow_circle_speed = 3
# красные круги это типо бомбы и очки уменьшатся
red_circle_speed = 4
blue_circle_speed = 5
yellow_circles = []
red_circles = []
blue_circles = []
score = 0
circle_timer = 2000
last_circle = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    k = pygame.key.get_pressed()
    if k[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if k[pygame.K_RIGHT] and player_x < w - player_size:
        player_x += player_speed

    current_time = pygame.time.get_ticks()
    if current_time - last_circle >= circle_timer:
        last_circle = current_time
        x = random.randint(circle_size, w - circle_size)
        y = -circle_size

        circle_type = random.choice(['yellow', 'red', 'blue'])
        if circle_type == 'yellow':
            yellow_circles.append([x, y])
        elif circle_type == 'red':
            red_circles.append([x, y])
        else:
            blue_circles.append([x, y])

    for i in range(len(yellow_circles) - 1, -1, -1):
        yellow_circles[i][1] += yellow_circle_speed
        circle_x = yellow_circles[i][0]
        circle_y = yellow_circles[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score += 10
            yellow_circles.pop(i)

        elif yellow_circles[i][1] > h + circle_size:
            yellow_circles.pop(i)

    for i in range(len(red_circles) - 1, -1, -1):
        red_circles[i][1] += red_circle_speed
        circle_x = red_circles[i][0]
        circle_y = red_circles[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score -= 15
            red_circles.pop(i)

        elif red_circles[i][1] > h + circle_size:
            red_circles.pop(i)

    for i in range(len(blue_circles) - 1, -1, -1):
        blue_circles[i][1] += blue_circle_speed
        circle_x = blue_circles[i][0]
        circle_y = blue_circles[i][1]

        if (player_x < circle_x + circle_size and player_x + player_size > circle_x - circle_size and
                player_y < circle_y + circle_size and player_y + player_size > circle_y - circle_size):
            score += 30
            blue_circles.pop(i)

        elif blue_circles[i][1] > h + circle_size:
            blue_circles.pop(i)

    screen.fill('black')
    pygame.draw.rect(screen, 'white', (player_x, player_y, player_size, player_size))

    for circle in yellow_circles:
        pygame.draw.circle(screen, 'yellow', (circle[0], circle[1]), circle_size)
    for circle in red_circles:
        pygame.draw.circle(screen, 'red', (circle[0], circle[1]), circle_size)
    for circle in blue_circles:
        pygame.draw.circle(screen, 'blue', (circle[0], circle[1]), circle_size)
    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}", True, 'white')
    screen.blit(text, (10, 10))
    pygame.display.flip()
    pygame.time.delay(30)
pygame.quit()
