import pygame
import random
import sqlite3

pygame.init()
w = 1700
h = 900
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("фруктомания")

player_size = 200
player_speed = 12
player_x = w // 2 - player_size // 2
player_y = h - player_size - 10

fruits_size = 70

banana_speed = 5
bomb_speed = 6
strawberry_speed = 8
oranges_speed = 5.5

bananas = []
bombs = []
strawberrys = []
oranges = []

score = 0
max_score = 0
fruits_timer = 2500
last_fruit = pygame.time.get_ticks()
contact_distance = 80


def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


banana_image = load_image("images/banana.png", (70, 70))
bomb_image = load_image("images/bomb.png", (80, 80))
strawberry_image = load_image("images/strawberry.png", (70, 70))
orange_image = load_image("images/orange.png", (70, 70))
background_image = load_image("images/background.png", (1200, h))
intro_image = load_image("images/intro.png", (w, h))
game_over_image = load_image("images/gameover.png", (w, h))
instruction_image = load_image("images/instruction.png", (600, 800))
settings_image = load_image("images/instruction_button.png", (300, 140))
play_image = load_image("images/play_button.png", (300, 140))
instruction_button_image = load_image("images/settings_button.png", (300, 140))
registration_image = load_image("images/registration_background.png", (300, 140))
registration_button = load_image("images/registration_button.png", (260, 140))
login_button = load_image("images/login_button.png", (260, 140))
back_button_image = load_image("images/back_button.png", (200, 100))
warning = load_image("images/warning.png", (900, 200))

player_can_play = False


login_screen = False
nickname = ""
password = ""
input_active = [False, False]

is_registered = False

conn = sqlite3.connect('fruitmania.db')
cursor = conn.cursor()


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
            a += 3
        else:
            a = 255
        instruction_image.set_alpha(a)
        screen.blit(instruction_image, (550, 50))
        pygame.display.flip()
        pygame.time.delay(5)


def show_warning():
    a = 0
    warning_running = True
    while warning_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                warning_running = False

        if a < 255:
            a += 3
        else:
            a = 255
        warning.set_alpha(a)
        screen.blit(warning, (370, 350))
        pygame.display.flip()
        pygame.time.delay(5)


def start_game():
    global player_x, player_y, score, bananas, bombs, strawberrys, oranges, last_fruit
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
        if current_time - last_fruit >= fruits_timer:
            last_fruit = current_time
            x = random.randint(fruits_size, 1150 - fruits_size)
            y = -fruits_size

            fruits_type = random.choice(['orange', 'bomb', 'banana', "strawberry"])
            if fruits_type == 'orange':
                oranges.append([x, y])
            elif fruits_type == 'bomb':
                bombs.append([x, y])
            elif fruits_type == 'banana':
                bananas.append([x, y])
            else:
                strawberrys.append([x, y])

        handle_fruits(bananas, banana_speed, 10)
        handle_fruits(bombs, bomb_speed, -15, is_bomb=True)
        handle_fruits(strawberrys, strawberry_speed, 30)
        handle_fruits(oranges, oranges_speed, 20)

        draw_game()
        pygame.display.flip()
        pygame.time.delay(5)


def handle_fruits(fruit_list, speed, score_change, is_bomb=False):
    global score
    for i in range(len(fruit_list) - 1, -1, -1):
        fruit_list[i][1] += speed
        circle_x, circle_y = fruit_list[i]

        if (abs(player_x - circle_x) < contact_distance and
                abs(player_y - circle_y) < contact_distance):
            score += score_change
            fruit_list.pop(i)
        elif fruit_list[i][1] > h + fruits_size:
            fruit_list.pop(i)

    for banana in bananas:
        screen.blit(banana_image, (banana[0], banana[1]))
    for bomb in bombs:
        screen.blit(bomb_image, (bomb[0], bomb[1]))
    for strawberry in strawberrys:
        screen.blit(strawberry_image, (strawberry[0], strawberry[1]))
    for orange in oranges:
        screen.blit(orange_image, (orange[0], orange[1]))

    pygame.display.flip()
    pygame.time.delay(5)


def draw_game():
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
                if (670 < mouse_x < 970) and (350 < mouse_y < 490) and player_can_play:
                    intro_running = False
                    start_game()
                if (670 < mouse_x < 970) and (350 < mouse_y < 490) and not player_can_play:
                    show_warning()
                if (670 < mouse_x < 870) and (450 < mouse_y < 550):
                    font = pygame.font.Font(None, 30)
                    text = font.render("(Чтобы закрыть инструкцию нажмите любую кнопку на клавиатуре)", True, 'white')
                    screen.blit(text, (500, 840))
                    show_instructions()
                if (290 < mouse_x < 550) and (770 < mouse_y < 910) and not is_registered:
                    show_registration()

        screen.blit(intro_image, (0, 0))
        screen.blit(settings_image, (670, 450))
        screen.blit(instruction_button_image, (670, 550))
        screen.blit(play_image, (670, 350))

        if not is_registered:
            screen.blit(login_button, (20, 770))
            screen.blit(registration_button, (290, 770))
        else:
            font = pygame.font.Font(None, 55)
            text = font.render(nickname, True, 'white')
            screen.blit(text, (20, 850))

        pygame.display.flip()
        pygame.time.delay(5)


def show_registration():
    global player_can_play, nickname, is_registered
    settings_running = True
    nickname = ''
    password = ''
    input_active = False
    cursor_visible = True
    cursor_timer = 0
    is_nickname_done = False

    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not is_nickname_done:
                        is_nickname_done = True
                    else:
                        player_can_play = True
                        is_registered = True
                elif event.key == pygame.K_BACKSPACE:
                    if input_active:
                        if len(password) > 0:
                            password = password[:-1]
                    else:
                        if len(nickname) > 0:
                            nickname = nickname[:-1]
                elif event.key == pygame.K_TAB:
                    input_active = not input_active
                elif event.key == pygame.K_ESCAPE:
                    settings_running = False
                elif input_active:
                    if event.unicode and event.unicode.isprintable():
                        password += event.unicode
                else:
                    if event.unicode and event.unicode.isprintable():
                        nickname += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    settings_running = False

        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        screen.blit(intro_image, (0, 0))

        overlay_surface = pygame.Surface((600, 800))
        overlay_surface.set_alpha(130)
        overlay_surface.fill((0, 0, 0, 200))
        screen.blit(overlay_surface, (550, 0))

        font = pygame.font.Font(None, 50)
        text = font.render("Регистрация аккаунта", True, 'white')
        screen.blit(text, (650, 50))

        text_nickname = font.render(f"Имя игрока: {nickname}", True, 'white')
        nickname_rect = text_nickname.get_rect(topleft=(600, 400))
        pygame.draw.rect(screen, 'white', nickname_rect.inflate(10, 10), 2)
        screen.blit(text_nickname, nickname_rect)

        text_password = font.render(f"Пароль: {'*' * len(password)}", True, 'white')
        password_rect = text_password.get_rect(topleft=(600, 500))
        pygame.draw.rect(screen, 'white', password_rect.inflate(10, 10), 2)
        screen.blit(text_password, password_rect)

        if input_active and cursor_visible:
            cursor_x = password_rect.x + text_password.get_width() + 10 if password else password_rect.x + 10
            cursor_y = password_rect.y + 10
            pygame.draw.line(screen, 'white', (cursor_x, cursor_y), (cursor_x, cursor_y + 40), 2)

        if is_nickname_done:
            input_active = True

        back_button_rect = back_button_image.get_rect(center=(w // 2, h - 100))
        screen.blit(back_button_image, back_button_rect)

        pygame.display.flip()
        pygame.time.delay(100)


show_intro()
conn.close()
pygame.quit()