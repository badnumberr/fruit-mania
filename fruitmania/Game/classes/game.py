import random
from player import Player
from constants import *

pygame.init()
pygame.mixer.init()


fruit_sound = pygame.mixer.Sound("../music/fruit.mp3")


def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


banana_image = load_image("../images/banana.png", (70, 70))
bomb_image = load_image("../images/bomb.png", (80, 80))
strawberry_image = load_image("../images/strawberry.png", (70, 70))
orange_image = load_image("../images/orange.png", (70, 70))
background_image = load_image("../images/background.png", (1200, H))
intro_image = load_image("../images/intro.png", (W, H))
instruction_image = load_image("../images/instruction.png", (600, 800))
settings_image = load_image("../images/instruction_button.png", (300, 140))
play_image = load_image("../images/play_button.png", (300, 140))
instruction_button_image = load_image("../images/settings_button.png", (300, 140))
registration_button = load_image("../images/registration_button.png", (260, 140))
login_button = load_image("../images/login_button.png", (260, 140))
back_button_image = load_image("../images/back_button.png", (180, 90))
warning = load_image("../images/warning.png", (900, 200))
monkey_image = load_image("../images/monkey.png", (140, 200))
monkey_over_image = load_image("../images/monkey_over.png", (140, 200))
pause_image = load_image("../images/pause.png", (180, 90))
continue_image = load_image("../images/continue.png", (400, 200))
intro_open_image = load_image("../images/intro_open.png", (400, 200))
level1_image = load_image("../images/level1.png", (400, 200))
level2_image = load_image("../images/level2.png", (400, 200))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H))
        self.player_x = W // 2 - PLAYER_SIZE // 2
        self.player_y = H - PLAYER_SIZE - 10
        self.score = 0
        self.bananas = []
        self.bombs = []
        self.strawberries = []
        self.oranges = []
        self.game_running = False
        self.player = Player()
        self.input_active = False
        self.warning = False
        self.max_score_for_win = 150
        self.cursor_visible = True
        self.cursor_timer = 0

    def reset_game(self):
        self.player_x = W // 2 - PLAYER_SIZE // 2
        self.player_y = H - PLAYER_SIZE - 10
        self.score = 0
        self.bananas.clear()
        self.bombs.clear()
        self.strawberries.clear()
        self.oranges.clear()
        self.last_fruit = pygame.time.get_ticks()
        self.game_running = False
        self.player_can_play = False
        self.game_over_running = False
        self.game_win_running = False

    def start_game(self, level=1):
        pygame.mixer.music.load("../music/game.mp3")
        pygame.mixer.music.play(-1)

        self.player_x = W // 2 - PLAYER_SIZE // 2
        self.player_y = H - PLAYER_SIZE - 10
        self.score = 0
        self.bananas.clear()
        self.bombs.clear()
        self.strawberries.clear()
        self.oranges.clear()
        self.last_fruit = pygame.time.get_ticks()
        self.game_running = True

        if level == 1:
            FRUITS_TIMER = 2500
            BANANA_SPEED = 5
            BOMB_SPEED = 6
            STRAWBERRY_SPEED = 8
            ORANGE_SPEED = 5.5
        elif level == 2:
            FRUITS_TIMER = 1500
            BANANA_SPEED = 7
            BOMB_SPEED = 4
            STRAWBERRY_SPEED = 10
            ORANGE_SPEED = 8

        while self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (1500 < mouse_x < 1700) and (10 < mouse_y < 100):
                        self.game_over()
                        self.game_running = False
                        self.show_intro()
                    if (1310 < mouse_x < 1490) and (10 < mouse_y < 100):
                        self.pause_game()

            k = pygame.key.get_pressed()
            if k[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= PLAYER_SPEED
            if k[pygame.K_RIGHT] and self.player_x < 1050:
                self.player_x += PLAYER_SPEED

            current_time = pygame.time.get_ticks()
            if current_time - self.last_fruit >= FRUITS_TIMER:
                self.last_fruit = current_time
                x = random.randint(FRUITS_SIZE, 1150 - FRUITS_SIZE)
                y = -FRUITS_SIZE

                if level == 1:
                    if random.random() < 0.3:
                        self.bombs.append([x, y])
                    else:
                        fruits_type = random.choice(['orange', 'banana', "strawberry"])
                        if fruits_type == 'orange':
                            self.oranges.append([x, y])
                        elif fruits_type == 'banana':
                            self.bananas.append([x, y])
                        else:
                            self.strawberries.append([x, y])
                elif level == 2:
                    if random.random() < 0.6:
                        self.bombs.append([x, y])
                    else:
                        fruits_type = random.choice(['orange', 'banana', "strawberry"])
                        if fruits_type == 'orange':
                            self.oranges.append([x, y])
                        elif fruits_type == 'banana':
                            self.bananas.append([x, y])
                        else:
                            self.strawberries.append([x, y])
            self.handle_fruits(self.bananas, BANANA_SPEED, 10)
            self.handle_fruits(self.bombs, BOMB_SPEED, -15, is_bomb=True)
            self.handle_fruits(self.strawberries, STRAWBERRY_SPEED, 30)
            self.handle_fruits(self.oranges, ORANGE_SPEED, 20)

            self.draw_game()
            pygame.display.flip()
            pygame.time.delay(20)

    def draw_game(self):
        SCREEN.fill('black')
        SCREEN.blit(background_image, (0, 0))

        player_image = pygame.image.load("../images/player.png")
        player_image = pygame.transform.scale(player_image, (140, 200))
        SCREEN.blit(player_image, (self.player_x, self.player_y))

        for banana in self.bananas:
            SCREEN.blit(banana_image, (banana[0], banana[1]))
        for bomb in self.bombs:
            SCREEN.blit(bomb_image, (bomb[0], bomb[1]))
        for strawberry in self.strawberries:
            SCREEN.blit(strawberry_image, (strawberry[0], strawberry[1]))
        for orange in self.oranges:
            SCREEN.blit(orange_image, (orange[0], orange[1]))

        SCREEN.blit(pause_image, (1310, 10))
        SCREEN.blit(back_button_image, (1500, 10))

        font = pygame.font.Font(None, 50)
        text = font.render(f"Рекорд игрока: {self.score}", True, 'white')
        SCREEN.blit(text, (1220, 840))

        text = font.render(f"Игрок: {self.player.nickname}", True, 'white')
        SCREEN.blit(text, (1220, 790))

    def pause_game(self):
        paused = True
        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        paused = False
                        pygame.mixer.music.unpause()
                    if event.key == pygame.K_d:
                        paused = False
                        pygame.mixer.music.unpause()
                        self.show_intro()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (350 < mouse_x < 750) and (350 < mouse_y < 650):
                        paused = False
                        pygame.mixer.music.unpause()
                    if (900 < mouse_x < 1300) and (350 < mouse_y < 650):
                        paused = False
                        pygame.mixer.music.unpause()
                        self.show_intro()

            overlay_surface = pygame.Surface((W, H))
            overlay_surface.fill((0, 0, 0))
            overlay_surface.set_alpha(130)
            SCREEN.blit(overlay_surface, (0, 0))

            SCREEN.blit(continue_image, (350, 350))
            SCREEN.blit(intro_open_image, (900, 350))

            pygame.display.flip()
            pygame.time.delay(20)

    def handle_fruits(self, fruit_list, speed, score_change, is_bomb=False):
        self.game_running = True
        for i in range(len(fruit_list) - 1, -1, -1):
            fruit_list[i][1] += speed
            circle_x, circle_y = fruit_list[i]

            if is_bomb and (
                    abs(self.player_x - circle_x) < CONTACT_DISTANCE and abs(self.player_y - circle_y) < CONTACT_DISTANCE):
                self.game_over()
                self.game_running = False
                return

            if (not is_bomb) and (
                    abs(self.player_x - circle_x) < CONTACT_DISTANCE and abs(self.player_y - circle_y) < CONTACT_DISTANCE):
                fruit_sound.play()
                self.score += score_change
                fruit_list.pop(i)

            elif fruit_list[i][1] > H + FRUITS_SIZE:
                fruit_list.pop(i)

        if self.score >= self.max_score_for_win:
            self.score = self.max_score_for_win
            self.game_win()

        for banana in self.bananas:
            SCREEN.blit(banana_image, (banana[0], banana[1]))
        for bomb in self.bombs:
            SCREEN.blit(bomb_image, (bomb[0], bomb[1]))
        for strawberry in self.strawberries:
            SCREEN.blit(strawberry_image, (strawberry[0], strawberry[1]))
        for orange in self.oranges:
            SCREEN.blit(orange_image, (orange[0], orange[1]))

    def show_intro(self):
        pygame.mixer.music.load("../music/intro.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
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

                    if (670 < mouse_x < 970) and (350 < mouse_y < 490):
                        intro_running = False
                        self.show_level_selection()

                    if (670 < mouse_x < 870) and (450 < mouse_y < 550):
                        font = pygame.font.Font(None, 30)
                        text = font.render("(Чтобы закрыть инструкцию нажмите любую кнопку на клавиатуре)", True,
                                           'white')
                        SCREEN.blit(text, (500, 840))
                        self.show_instructions()

                    if (290 < mouse_x < 550) and (770 < mouse_y < 910) and not self.player.is_registered:
                        self.show_registration()
                    if self.player.is_registered and (20 < mouse_x < 200) and (770 < mouse_y < 910):
                        self.player.show_player_info(self)
                    if (20 < mouse_x < 200) and (770 < mouse_y < 910):
                        self.show_login()

            SCREEN.blit(intro_image, (0, 0))
            SCREEN.blit(play_image, (670, 350))
            SCREEN.blit(settings_image, (670, 450))
            SCREEN.blit(instruction_button_image, (670, 550))

            if self.player.is_registered:
                font = pygame.font.Font(None, 55)
                text = font.render(f"Игрок: {self.player.nickname}", True, 'white')
                SCREEN.blit(text, (25, 840))

            if not self.player.is_registered:
                SCREEN.blit(login_button, (20, 770))
                SCREEN.blit(registration_button, (290, 770))

            pygame.display.flip()
            pygame.time.delay(20)

    def show_instructions(self):
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
            SCREEN.blit(instruction_image, (550, 50))
            pygame.display.flip()
            pygame.time.delay(5)

    def show_warning(self):
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
            SCREEN.blit(warning, (370, 350))
            pygame.display.flip()
            pygame.time.delay(5)

        self.show_intro()

    def game_over(self):
        pygame.mixer.music.load("../music/game_over.mp3")
        pygame.mixer.music.play(-1)
        self.game_running = False
        if self.score > self.player.max_score:
            self.player.max_score = self.score
            self.player.save_player_data()

        monkey_x = W // 2 - 250
        monkey_y = H // 2

        dance_direction = 1
        dance_amplitude = 10
        dance_speed = 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.show_intro()
                        return

            SCREEN.fill('black')
            SCREEN.blit(background_image, (0, 0))

            monkey_y += dance_direction * dance_speed
            if monkey_y > H // 2 + dance_amplitude or monkey_y < H // 2 - dance_amplitude:
                dance_direction *= -1

            scaled_monkey_image = pygame.transform.scale(monkey_over_image, (500, 540))
            SCREEN.blit(scaled_monkey_image, (monkey_x, monkey_y - (scaled_monkey_image.get_height() - 500) // 2))

            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Игра Окончена", True, (255, 0, 0))
            SCREEN.blit(game_over_text, (W // 2 - game_over_text.get_width() // 2, H // 2 - 50))

            final_score_text = font.render(f"Ваш счет: {self.score}", True, (255, 255, 0))
            SCREEN.blit(final_score_text, (W // 2 - final_score_text.get_width() // 2, H // 2 + 10))

            return_button_text = font.render("Нажмите Enter, чтобы вернуться", True, (255, 255, 255))
            SCREEN.blit(return_button_text, (W // 2 - return_button_text.get_width() // 2, H // 2 + 70))

            pygame.display.flip()
            pygame.time.delay(20)

    def show_level_selection(self):
        if not self.player.is_registered:
            self.show_warning()
            return
        level_selection_running = True
        while level_selection_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    level_selection_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        level_selection_running = False
                        self.show_intro()

                    if level1_rect.collidepoint(mouse_x, mouse_y):
                        self.start_game(level=1)
                        return

                    elif level2_rect.collidepoint(mouse_x, mouse_y):
                        self.start_game(level=2)
                        return

            SCREEN.fill('black')
            SCREEN.blit(intro_image, (0, 0))

            text_y_position = H // 2 + 100

            level1_rect = SCREEN.blit(level1_image, (W // 2 - 500, H // 2 - 100))
            font = pygame.font.Font(None, 36)
            level1_text = font.render("Уровень сложности: ЛЕГКИЙ", True, 'white')

            level1_background = pygame.Surface((level1_text.get_width() + 20, level1_text.get_height() + 20))
            level1_background.set_alpha(150)
            level1_background.fill((0, 0, 0))
            SCREEN.blit(level1_background, (W // 2 - 490, text_y_position - 10))
            SCREEN.blit(level1_text, (W // 2 - 480, text_y_position))

            level2_rect = SCREEN.blit(level2_image, (W // 2 + 130, H // 2 - 100))
            level2_text = font.render("Уровень сложности: СЛОЖНЫЙ", True, 'red')

            level2_background = pygame.Surface((level2_text.get_width() + 20, level2_text.get_height() + 20))
            level2_background.set_alpha(150)
            level2_background.fill((0, 0, 0))
            SCREEN.blit(level2_background, (W // 2 + 130 - 10, text_y_position - 10))
            SCREEN.blit(level2_text, (W // 2 + 130, text_y_position))

            back_button_rect = back_button_image.get_rect(center=(W // 2, H - 100))
            SCREEN.blit(back_button_image, back_button_rect)

            pygame.display.flip()
            pygame.time.delay(20)

    def game_win(self):
        pygame.mixer.music.load("../music/game_win.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)
        self.game_running = False
        self.game_over_running = False
        if self.score > self.player.max_score:
            self.player.max_score = self.score
            self.player.save_player_data()

        monkey_x = W // 2 - 250
        monkey_y = H // 2

        dance_direction = 2
        dance_amplitude = 10
        dance_speed = 5

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        return

            SCREEN.fill('black')
            SCREEN.blit(background_image, (0, 0))

            monkey_y += dance_direction * dance_speed
            if monkey_y > H // 2 + dance_amplitude or monkey_y < H // 2 - dance_amplitude:
                dance_direction *= -1

            scaled_monkey_image = pygame.transform.scale(monkey_image, (500, 540))
            SCREEN.blit(scaled_monkey_image, (monkey_x, monkey_y - (scaled_monkey_image.get_height() - 500) // 2))

            SCREEN.blit(scaled_monkey_image, (monkey_x, monkey_y - (scaled_monkey_image.get_height() - 500) // 2))

            font = pygame.font.Font(None, 72)
            win_text = font.render("Победа!", True, (0, 255, 0))
            SCREEN.blit(win_text, (W // 2 - win_text.get_width() // 2, H // 2 - 50))

            final_score_text = font.render(f"Ваш счет: {self.max_score_for_win}", True, (255, 255, 0))
            SCREEN.blit(final_score_text, (W // 2 - final_score_text.get_width() // 2, H // 2 + 10))

            return_button_text = font.render("Нажмите Enter, чтобы вернуться", True, (255, 255, 255))
            SCREEN.blit(return_button_text, (W // 2 - return_button_text.get_width() // 2, H // 2 + 70))

            pygame.display.flip()
            pygame.time.delay(20)

    def show_login(self):
        self.login_running = True
        self.password = ""
        input_active = 0
        cursor_visible = True
        cursor_timer = 0

        while self.login_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.login_running = False

                    if event.key == pygame.K_RETURN:
                        if input_active == 0:
                            self.player.nickname = self.player.nickname.strip()
                            self.player.load_data()
                            if self.player.is_registered:
                                input_active = 1
                        elif input_active == 1:
                            if self.player.password == self.player.current_player_data[self.player.nickname]['password']:
                                self.player.is_registered = True
                                self.login_running = False

                    elif event.key == pygame.K_BACKSPACE:
                        if input_active == 0 and len(self.player.nickname) > 0:
                            self.player.nickname = self.player.nickname[:-1]
                        elif input_active == 1 and len(self.password) > 0:
                            self.password = self.password[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        if input_active == 0 and len(self.player.nickname) < 20:
                            self.player.nickname += event.unicode
                        elif input_active == 1 and len(self.password) < 20:
                            self.password += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    nickname_rect = pygame.Rect(600, 400, 300, 50)
                    password_rect = pygame.Rect(600, 500, 300, 50)
                    back_button_rect = pygame.Rect(W // 2 - 90, H - 100, 180, 90)

                    if nickname_rect.collidepoint(mouse_x, mouse_y):
                        input_active = 0
                    elif password_rect.collidepoint(mouse_x, mouse_y):
                        input_active = 1
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        self.login_running = False

            cursor_timer += 1
            if cursor_timer >= 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            SCREEN.blit(intro_image, (0, 0))

            overlay_surface = pygame.Surface((600, 800))
            overlay_surface.set_alpha(130)
            overlay_surface.fill((0, 0, 0, 200))
            SCREEN.blit(overlay_surface, (550, 0))

            font = pygame.font.Font(None, 50)
            title_text = font.render("Вход в аккаунт", True, 'white')
            SCREEN.blit(title_text, (650, 50))

            nickname_text = font.render(f"Имя игрока: {self.player.nickname}", True, 'white')
            nickname_rect = pygame.Rect(600, 400, 300, 50)
            pygame.draw.rect(SCREEN, 'white', nickname_rect, 2)
            SCREEN.blit(nickname_text, (nickname_rect.x + 10, nickname_rect.y + 10))

            password_text = font.render(f"Пароль: {'*' * len(self.password)}", True, 'white')
            password_rect = pygame.Rect(600, 500, 300, 50)
            pygame.draw.rect(SCREEN, 'white', password_rect, 2)
            SCREEN.blit(password_text, (password_rect.x + 10, password_rect.y + 10))

            if input_active == 1 and cursor_visible:
                cursor_x = password_rect.x + password_text.get_width() + 10 if self.password else password_rect.x + 10
                cursor_y = password_rect.y + 10
                pygame.draw.line(SCREEN, 'white', (cursor_x, cursor_y), (cursor_x, cursor_y + 40), 2)

            login_button_image = load_image("../images/login_button.png", (180, 90))
            login_button_rect = login_button_image.get_rect(center=(W // 2, 650))
            SCREEN.blit(login_button_image, login_button_rect)

            back_button_image = load_image("../images/back_button.png", (180, 90))
            back_button_rect = back_button_image.get_rect(center=(W // 2, H - 100))
            SCREEN.blit(back_button_image, back_button_rect)

            pygame.display.flip()
            pygame.time.delay(20)

    def show_registration(self):
        settings_running = True
        is_nickname_done = False
        self.input_active = 0

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
                            success = self.player.register_player(self.player.nickname, self.player.password)
                            if success:
                                self.player.is_registered = True
                                settings_running = False
                    elif event.key == pygame.K_BACKSPACE:
                        if self.input_active == 1 and len(self.player.password) > 0:
                            self.player.password = self.player.password[:-1]
                        elif self.input_active == 0 and len(self.player.nickname) > 0:
                            self.player.nickname = self.player.nickname[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        settings_running = False
                    elif event.unicode and event.unicode.isprintable():
                        if self.input_active == 0 and len(self.player.nickname) < 20:
                            self.player.nickname += event.unicode
                        elif self.input_active == 1 and len(self.player.password) < 20:
                            self.player.password += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    nickname_rect = pygame.Rect(600, 400, 300, 50)
                    password_rect = pygame.Rect(600, 500, 300, 50)
                    if nickname_rect.collidepoint(mouse_x, mouse_y):
                        self.input_active = 0
                    elif password_rect.collidepoint(mouse_x, mouse_y):
                        self.input_active = 1
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        settings_running = False

                self.cursor_timer += 1
                if self.cursor_timer >= 30:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = 0

                SCREEN.blit(intro_image, (0, 0))

                overlay_surface = pygame.Surface((600, 800))
                overlay_surface.set_alpha(130)
                overlay_surface.fill((0, 0, 0, 200))
                SCREEN.blit(overlay_surface, (550, 0))

                font = pygame.font.Font(None, 50)
                text = font.render("Регистрация аккаунта", True, 'white')
                SCREEN.blit(text, (650, 50))

                text_nickname = font.render(f"Имя игрока: {self.player.nickname}", True, 'white')
                nickname_rect = text_nickname.get_rect(topleft=(600, 400))
                pygame.draw.rect(SCREEN, 'white', nickname_rect.inflate(10, 10), 2)
                SCREEN.blit(text_nickname, nickname_rect)

                text_password = font.render(f"Пароль: {'*' * len(self.player.password)}", True, 'white')
                password_rect = text_password.get_rect(topleft=(600, 500))
                pygame.draw.rect(SCREEN, 'white', password_rect.inflate(10, 10), 2)
                SCREEN.blit(text_password, password_rect)

                if self.input_active == 1 and self.cursor_visible:
                    cursor_x = password_rect.x + text_password.get_width() + 10 if self.player.password else password_rect.x + 10
                    cursor_y = password_rect.y + 10
                    pygame.draw.line(SCREEN, 'white', (cursor_x, cursor_y), (cursor_x, cursor_y + 40), 2)

                if is_nickname_done:
                    self.input_active = 1
                back_button_rect = back_button_image.get_rect(center=(W // 2, H - 100))
                SCREEN.blit(back_button_image, back_button_rect)

                pygame.display.flip()
                pygame.time.delay(100)

