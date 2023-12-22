import sys
import pygame
from settings import *
from level import Level
from overworld import Overworld
from ui import UI, Menu, End


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Здоровье и кол-во собранных монет
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        self.status = 'menu'

        # Создание внешнего мира
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_lvl)

        # Интерфейс во время игры
        self.ui = UI(self.screen)

    def change_health(self, amount):
        self.current_health += amount

    def change_scores(self, amount):
        self.coins += amount

    # Осуществление проверки падения здоровья игрока до нуля
    def check_endgame(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.overworld = Overworld(0, self.max_level, self.screen, self.create_lvl)
            self.status = 'overworld'

    # Создание уровня
    def create_lvl(self, current_level):
        self.level = Level(current_level, self.screen, self.create_overworld, self.change_scores,
                           self.change_health, self.current_health, self.check_endgame, self)
        self.current_health = 100
        self.status = 'level'

    # Создание внешнего мира
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_lvl)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()

        elif self.status == 'menu':
            menu.draw(self.screen)

        elif self.status == 'end':
            end.draw(self.screen)

        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_scores(self.coins)
            self.check_endgame()

    def start_game(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                menu.start_button.event_control(event, pygame.mouse.get_pos())
                menu.quit_button.event_control(event, pygame.mouse.get_pos())

                end.menu_button.event_control(event, pygame.mouse.get_pos())

            self.run()
            pygame.display.set_caption(f"{game_name}")
            pygame.display.set_icon(pygame.image.load('../graphics/icon/helmet.png'))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    menu = Menu("../graphics/ui/button01.png", game)
    end = End("../graphics/ui/button01.png", game)
    game.start_game()
