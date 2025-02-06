from constants import *
import sqlite3
import datetime


pygame.init()
pygame.mixer.init()


def load_image(path, size):  # обработка изображений
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


class Player:  # инизиализация необходимых переменных
    def __init__(self):
        self.nickname = ""
        self.password = ""
        self.max_score = 0
        self.is_registered = False
        self.current_player_data = {}
        self.registration_date = ''

    def login(self, nickname, password):  # функция проверяет успешно ли прошел вход в аккаунт
        self.nickname = nickname
        self.load_data()

        if self.is_registered and self.password == password:
            return True
        else:
            self.is_registered = False
            return False

    def load_data(self):  # выгружат данные об игроке из базы данных
        conn = sqlite3.connect('../fruitmania_database/players.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM players WHERE nickname=?", (self.nickname,))
        result = cursor.fetchone()

        if result:
            self.is_registered = True
            self.password = result[1]
            self.max_score = int(result[2])
            self.current_player_data[self.nickname] = {
                'password': self.password,
                'max_score': self.max_score
            }
        else:
            self.is_registered = False

        conn.close()

    def register_player(self, nickname, password):
        conn = sqlite3.connect('../fruitmania_database/players.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players WHERE nickname = ?", (nickname,))
        if cursor.fetchone() is not None:
            conn.close()
            return False
        registration_date = datetime.datetime.now().strftime('%d-%m-%Y')
        cursor.execute("INSERT INTO players (nickname, password, max_score, registration_date) VALUES (?, ?, ?, ?)",
                       (nickname, password, 0, registration_date))
        conn.commit()
        conn.close()
        self.current_player_data[nickname] = {
            'password': password,
            'max_score': 0,
            'registration_date': registration_date
        }
        self.is_registered = True
        return True

    def save_player_data(self):  # сохраняет новые данные об игроке в БД
        if self.nickname in self.current_player_data:
            current_max_score = self.current_player_data[self.nickname]['max_score']
            new_max_score = max(current_max_score, self.max_score)

            conn = sqlite3.connect('../fruitmania_database/players.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE players SET max_score=? WHERE nickname=?", (new_max_score, self.nickname))
            conn.commit()
            conn.close()

            self.current_player_data[self.nickname]['max_score'] = new_max_score

    def load_last_player(self):  # выгружает данные о последнем игроке
        try:
            with open(LAST_PLAYER_FILE, 'r', encoding='utf-8') as file:
                last_player_name = file.readline().strip()
                if last_player_name in self.current_player_data:
                    nickname = last_player_name
                    self.max_score = self.current_player_data[nickname]['max_score']
                    self.registration_date = datetime.datetime.now().strftime("%d-%m-%Y")
                    self.is_registered = True
        except FileNotFoundError:
            print("Файл с последним игроком не найден.")

    def save_last_player(self):  # сохраняет данные о последнем игроке в текстовый файл
        with open(LAST_PLAYER_FILE, 'w', encoding='utf-8') as file:
            file.write(self.nickname)

    def show_player_info(self, game_instance):  # открывает окно с показом информации об игроке
        self.game = game_instance
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
                        self.game.show_intro()
                        info_running = False
                    if logout_button_rect.collidepoint(mouse_x, mouse_y):
                        self.logout()
                        info_running = False

            overlay_surface = pygame.Surface((600, 800))
            overlay_surface.set_alpha(130)
            overlay_surface.fill((0, 0, 0))
            SCREEN.blit(overlay_surface, (550, 0))

            font = pygame.font.Font(None, 50)
            title_text = font.render("Информация о игроке", True, 'white')
            SCREEN.blit(title_text, (W // 2 - title_text.get_width() // 2, 50))

            nickname_text = font.render(f"Никнейм: {self.nickname}", True, 'white')
            score_text = font.render(f"Максимальный счет: {self.max_score}", True, 'white')
            registration_text = font.render(f"Дата регистрации: {self.registration_date}", True, 'white')

            SCREEN.blit(nickname_text, (W // 2 - nickname_text.get_width() // 2, 150))
            SCREEN.blit(score_text, (W // 2 - score_text.get_width() // 2, 200))
            SCREEN.blit(registration_text, (W // 2 - registration_text.get_width() // 2, 250))

            back_button_image = load_image("../images/back_button.png", (180, 90))

            logout_button_image = load_image("../images/logout.png", (180, 90))
            back_button_rect = back_button_image.get_rect(center=(660, H - 140))
            logout_button_rect = logout_button_image.get_rect(center=(1040, H - 140))

            SCREEN.blit(back_button_image, back_button_rect)
            SCREEN.blit(logout_button_image, logout_button_rect)

            pygame.display.flip()
            pygame.time.delay(5)


    def logout(self):  # сбрасывает все данные в игре после выхода из аккаунта
        self.save_player_data()
        self.nickname = ""
        self.password = ""
        self.is_registered = False
        self.max_score = 0
        self.current_player_data = {}
        self.clear_last_player_file()
        self.game.show_intro()

    def clear_last_player_file(self):  # после выхода из аккаунта очищает файл с последним игроком
        with open(LAST_PLAYER_FILE, 'w', encoding='utf-8') as file:
            file.write("")
