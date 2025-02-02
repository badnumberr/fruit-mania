import pygame
from game import Game
from player import Player


def main():
    player = Player()
    game = Game()
    game.show_intro()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if player.is_registered:
            game.start_game()
        else:

            if game.show_registration():
                player.register_player(player.nickname, player.password)


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()