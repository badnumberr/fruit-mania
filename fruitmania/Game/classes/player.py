from constants import *
import sqlite3
from datetime import datetime


pygame.init()
pygame.mixer.init()


def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return None


back_button_image = load_image("../images/back_button.png", (180, 90))
login_screen = False
input_active = [False, False]
last_player_file = '../registered_players/last_player.txt'


class Player:
    def __init__(self):
        self.nickname = ""
        self.password = ""
        self.max_score = 0
        self.is_registered = False
        self.current_player_data = {}

    def load_data(self):
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM players WHERE nickname=?", (self.nickname,))
        result = cursor.fetchone()

        if result:
            self.is_registered = True
            self.password = result[2]
            self.max_score = result[3]
            self.current_player_data[self.nickname] = {
                'password': self.password,
                'max_score': self.max_score
            }
        else:
            self.is_registered = False

        conn.close()

    def register_player(self, nickname, password):
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO players (nickname, password, max_score, registration_date) VALUES (?, ?, ?, ?)",
                       (nickname, password, 0, registration_date))
        conn.commit()
        conn.close()

    def save_player_data(self):
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET max_score=? WHERE nickname=?", (self.max_score, self.nickname))
        conn.commit()
        conn.close()

    def show_player_info(self, game_instance):
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
            registration_text = font.render(f"Дата регистрации: {self.get_registration_date()}", True, 'white')

            SCREEN.blit(nickname_text, (W // 2 - nickname_text.get_width() // 2, 150))
            SCREEN.blit(score_text, (W // 2 - score_text.get_width() // 2, 200))
            SCREEN.blit(registration_text, (W // 2 - registration_text.get_width() // 2, 250))

            logout_button_image = load_image("../images/logout.png", (180, 90))
            back_button_rect = back_button_image.get_rect(center=(660, H - 140))
            logout_button_rect = logout_button_image.get_rect(center=(1040, H - 140))

            SCREEN.blit(back_button_image, back_button_rect)
            SCREEN.blit(logout_button_image, logout_button_rect)

            pygame.display.flip()
            pygame.time.delay(5)

    def get_registration_date(self):
        conn = sqlite3.connect('players.db')
        cursor = conn.cursor()
        cursor.execute("SELECT registration_date FROM players WHERE nickname=?", (self.nickname,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else "Неизвестно"

    def logout(self):
        from fruitmania.Game.classes.game import Game
        self.game = Game()
        self.nickname = ""
        self.password = ""
        self.is_registered = False
        self.max_score = 0
        self.registration_date = ''
        self.score = 0
        self.current_player_data = {}
        self.clear_last_player_file()
        self.game.show_intro()

    def clear_last_player_file(self):
        with open(LAST_PLAYER_FILE, 'w', encoding='utf-8') as file:
            file.write("")