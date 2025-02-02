from constants import *

pygame.init()
pygame.mixer.init()


fruit_sound = pygame.mixer.Sound("../music/fruit.mp3")
pause_sound = pygame.mixer.Sound("../music/pause.mp3")
game_over_sound = pygame.mixer.Sound("../music/game_over.mp3")
game_win_sound = pygame.mixer.Sound("../music/game_win.mp3")


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


class Fruit:
    def __init__(self):
        self.fruits_size = FRUITS_SIZE
        self.banana_speed = BANANA_SPEED
        self.bomb_speed = BOMB_SPEED
        self.strawberry_speed = STRAWBERRY_SPEED
        self.orange_speed = ORANGE_SPEED

    def handle_fruits(self, fruit_list, speed, score_change, is_bomb=False):
        from game import Game
        self.game = Game()
        self.game.game_running = True
        for i in range(len(fruit_list) - 1, -1, -1):
            fruit_list[i][1] += speed
            circle_x, circle_y = fruit_list[i]

            if is_bomb and (
                    abs(self.game.player_x - circle_x) < CONTACT_DISTANCE and abs(self.game.player_y - circle_y) < CONTACT_DISTANCE):
                self.game.game_over()
                self.game.game_running = False
                return

            if (not is_bomb) and (
                    abs(self.game.player_x - circle_x) < CONTACT_DISTANCE and abs(self.game.player_y - circle_y) < CONTACT_DISTANCE):
                fruit_sound.play()
                self.game.score += score_change
                fruit_list.pop(i)

            elif fruit_list[i][1] > H + FRUITS_SIZE:
                fruit_list.pop(i)

        if self.game.score >= self.game.max_score_for_win:
            self.game.score = self.game.max_score_for_win
            self.game.game_win()

        for banana in self.game.bananas:
            SCREEN.blit(banana_image, (banana[0], banana[1]))
        for bomb in self.game.bombs:
            SCREEN.blit(bomb_image, (bomb[0], bomb[1]))
        for strawberry in self.game.strawberries:
            SCREEN.blit(strawberry_image, (strawberry[0], strawberry[1]))
        for orange in self.game.oranges:
            SCREEN.blit(orange_image, (orange[0], orange[1]))

