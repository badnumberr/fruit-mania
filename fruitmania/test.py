import pygame
import random
import datetime


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
current_player_data = {}

data_file = 'registered_players/players_data.txt'

max_score_for_win = 50


def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


monkey_image = load_image("images/monkey.png", (140, 200))
monkey_x = player_x
monkey_y = player_y
monkey_speed = 15
monkey_scale = 1.0
scale_increment = 0.1
max_scale = 1.5

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
back_button_image = load_image("images/back_button.png", (180, 90))
warning = load_image("images/warning.png", (900, 200))

pause_image = load_image("images/pause.png", (180, 90))
continue_image = load_image("images/continue.png", (400, 200))
intro_open_image = load_image("images/intro_open.png", (400, 200))

player_can_play = False
game_running = True
game_over_running = True
game_win_running = True

login_screen = False
nickname = ""
password = ""
input_active = [False, False]
registration_date = ''
is_registered = False
last_player_file = 'registered_players/last_player.txt'


def save_data():
    with open(data_file, 'w', encoding='utf-8') as file:
        for player, data in current_player_data.items():
            file.write(f"{player},{data['password']},{data['max_score']}\n")


def save_last_player():
    with open(last_player_file, 'w', encoding='utf-8') as file:
        file.write(nickname)


def load_last_player():
    global nickname, max_score, registration_date, is_registered
    try:
        with open(last_player_file, 'r', encoding='utf-8') as file:
            last_player_name = file.readline().strip()
            if last_player_name in current_player_data:
                nickname = last_player_name
                max_score = current_player_data[nickname]['max_score']
                registration_date = datetime.datetime.now().strftime("%d-%m-%Y")
                is_registered = True
    except FileNotFoundError:
        print("Файл с последним игроком не найден.")


def save_player_data():
    global current_player_data, nickname, score
    if nickname in current_player_data:
        current_player_data[nickname]['max_score'] = max(current_player_data[nickname]['max_score'], score)
    save_data()
    save_last_player()


def load_data():
    global current_player_data
    current_player_data = {}
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    name, password, max_score_str = line.split(',')
                    current_player_data[name] = {
                        'password': password,
                        'max_score': int(max_score_str)
                    }
        load_last_player()
    except FileNotFoundError:
        print("Файл с данными игроков не найден. Создайте новых игроков.")


def register_player(nickname, password):
    if nickname in current_player_data:
        return False

    current_player_data[nickname] = {'password': password, 'max_score': 0}
    save_data()
    save_last_player()
    return True


def show_player_info():
    global nickname, max_score, registration_date
    info_running = True
    while info_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                info_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    info_running = False

        overlay_surface = pygame.Surface((600, 800))
        overlay_surface.set_alpha(130)
        overlay_surface.fill((0, 0, 0))
        screen.blit(overlay_surface, (550, 0))
        font = pygame.font.Font(None, 50)

        title_text = font.render("Информация о игроке", True, 'white')
        screen.blit(title_text, (w // 2 - title_text.get_width() // 2, 50))

        nickname_text = font.render(f"Никнейм: {nickname}", True, 'white')
        score_text = font.render(f"Максимальный счет: {max_score}", True, 'white')
        registration_text = font.render(f"Дата регистрации: {registration_date}", True, 'white')

        screen.blit(nickname_text, (w // 2 - nickname_text.get_width() // 2, 150))
        screen.blit(score_text, (w // 2 - score_text.get_width() // 2, 200))
        screen.blit(registration_text, (w // 2 - registration_text.get_width() // 2, 250))

        back_button_rect = back_button_image.get_rect(center=(w // 2, h - 100))
        screen.blit(back_button_image, back_button_rect)

        pygame.display.flip()
        pygame.time.delay(5)


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
    global game_running

    player_x = w // 2 - player_size // 2
    player_y = h - player_size - 10
    score = 0
    bananas.clear()
    bombs.clear()
    strawberrys.clear()
    oranges.clear()
    last_fruit = pygame.time.get_ticks()
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (1500 < mouse_x < 1700) and (10 < mouse_y < 100):
                    game_over()
                    game_running = False
                    show_intro()
                if (1310 < mouse_x < 1490) and (10 < mouse_y < 100):
                    pause_game()

        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if k[pygame.K_RIGHT] and player_x < 1050:
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
        pygame.time.delay(20)

    game_over()


def handle_fruits(fruit_list, speed, score_change, is_bomb=False):
    global score, game_running
    for i in range(len(fruit_list) - 1, -1, -1):
        fruit_list[i][1] += speed
        circle_x, circle_y = fruit_list[i]

        if is_bomb and (abs(player_x - circle_x) < contact_distance and abs(player_y - circle_y) < contact_distance):
            game_running = False
            return

        if (not is_bomb) and (abs(player_x - circle_x) < contact_distance and abs(player_y - circle_y) < contact_distance):
            score += score_change
            fruit_list.pop(i)
        elif fruit_list[i][1] > h + fruits_size:
            fruit_list.pop(i)

    if score >= max_score_for_win:
        score = max_score_for_win
        game_win()

    for banana in bananas:
        screen.blit(banana_image, (banana[0], banana[1]))
    for bomb in bombs:
        screen.blit(bomb_image, (bomb[0], bomb[1]))
    for strawberry in strawberrys:
        screen.blit(strawberry_image, (strawberry[0], strawberry[1]))
    for orange in oranges:
        screen.blit(orange_image, (orange[0], orange[1]))


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

    screen.blit(pause_image, (1310, 10))
    screen.blit(back_button_image, (1500, 10))


    font = pygame.font.Font(None, 50)
    text = font.render(f"Рекорд игрока: {score}", True, 'white')
    screen.blit(text, (1220, 840))

    text = font.render(f"Игрок: {nickname}", True, 'white')
    screen.blit(text, (1220, 790))


def game_over():
    global max_score, game_running, game_over_running, monkey_x, monkey_y
    game_running = False
    if score > max_score:
        max_score = score
        save_player_data()

    monkey_x = w // 2 - 250
    monkey_y = h // 2

    dance_direction = 1
    dance_amplitude = 10
    dance_speed = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill('black')
        screen.blit(background_image, (0, 0))

        monkey_y += dance_direction * dance_speed
        if monkey_y > h // 2 + dance_amplitude or monkey_y < h // 2 - dance_amplitude:
            dance_direction *= -1

        scaled_monkey_image = pygame.transform.scale(monkey_image, (500, 540))
        screen.blit(scaled_monkey_image, (monkey_x, monkey_y - (scaled_monkey_image.get_height() - 500) // 2))

        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Игра Окончена", True, (255, 0, 0))
        screen.blit(game_over_text, (w // 2 - game_over_text.get_width() // 2, h // 2 - 50))

        final_score_text = font.render(f"Ваш счет: {score}", True, (255, 255, 0))
        screen.blit(final_score_text, (w // 2 - final_score_text.get_width() // 2, h // 2 + 10))

        return_button_text = font.render("Нажмите Enter, чтобы вернуться", True, (255, 255, 255))
        screen.blit(return_button_text, (w // 2 - return_button_text.get_width() // 2, h // 2 + 70))

        pygame.display.flip()
        pygame.time.delay(20)

    while game_over_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_intro()
                    game_over_running = False



        pygame.display.flip()
        pygame.time.delay(100)


def game_win():
    global max_score, game_running, game_win_running
    game_running = False
    if score > max_score:
        max_score = score
        save_player_data()

    while game_win_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_intro()
                    game_win_running = False




        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Победа!", True, (255, 0, 0))
        screen.blit(game_over_text, (w // 2 - game_over_text.get_width() // 2, h // 2 - 50))

        final_score_text = font.render(f"Ваш счет: {max_score_for_win}", True, (255, 255, 0))
        screen.blit(final_score_text, (w // 2 - final_score_text.get_width() // 2, h // 2 + 10))

        return_button_text = font.render("Нажмите Enter, чтобы вернуться", True, (255, 255, 255))
        screen.blit(return_button_text, (w // 2 - return_button_text.get_width() // 2, h // 2 + 70))

        pygame.display.flip()
        pygame.time.delay(100)


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
                if (670 < mouse_x < 970) and (350 < mouse_y < 490) and nickname != "":
                    intro_running = False
                    start_game()
                if (670 < mouse_x < 970) and (350 < mouse_y < 490) and nickname == "":
                    show_warning()
                if (670 < mouse_x < 870) and (450 < mouse_y < 550):
                    font = pygame.font.Font(None, 30)
                    text = font.render("(Чтобы закрыть инструкцию нажмите любую кнопку на клавиатуре)", True, 'white')
                    screen.blit(text, (500, 840))
                    show_instructions()
                if (290 < mouse_x < 550) and (770 < mouse_y < 910) and not is_registered:
                    show_registration()
                if is_registered and (20 < mouse_x < 200) and (770 < mouse_y < 910):
                    show_player_info()

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
            screen.blit(text, (25, 840))

        pygame.display.flip()
        pygame.time.delay(5)


def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    paused = False
                if event.key == pygame.K_d:  #
                    show_intro()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (350 < mouse_x < 750) and (350 < mouse_y < 650):
                    paused = False
                    start_game()
                if (900 < mouse_x < 1300) and (350 < mouse_y < 650):
                    paused = False
                    show_intro()

        overlay_surface = pygame.Surface((w, h))
        overlay_surface.fill((0, 0, 0))
        overlay_surface.set_alpha(130)
        screen.blit(overlay_surface, (0, 0))

        screen.blit(continue_image, (350, 350))
        screen.blit(intro_open_image, (900, 350))

        pygame.display.flip()
        pygame.time.delay(20)


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
                        if register_player(nickname, password):
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
                    if event.unicode and event.unicode.isprintable() and len(password) < 8:
                        password += event.unicode
                else:
                    if event.unicode and event.unicode.isprintable() and len(nickname) < 8:
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


def main():
    load_data()
    show_intro()

    while True:
        if player_can_play:
            start_game()


if __name__ == "__main__":
    main()
    pygame.quit()