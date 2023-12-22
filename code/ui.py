import pygame
import settings
from button import Button
from text_drawer import drawtext

class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # Монеты
        self.coin = pygame.image.load('../graphics/ui/coin1.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        # Здоровье
        self.health_bar = pygame.image.load('../graphics/ui/health_bar2.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_length = 152
        self.bar_height = 4

        # Шрифт
        self.font = pygame.font.Font('../graphics/ui/font.ttf', 20)

    def show_health(self, curr, full):
        self.display_surface.blit(self.health_bar, (20, 10))
        curr_health_ratio = curr / full
        curr_bar_length = self.bar_max_length * curr_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (curr_bar_length, self.bar_height))
        pygame.draw.rect(self.display_surface, '#AD4A19', health_bar_rect)

    def show_scores(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount = self.font.render(str(amount), False, '#EEE8AA')
        coin_amount_rect = coin_amount.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount, coin_amount_rect)


# Класс интерфейса меню
class Menu:
    def __init__(self, buttons_image_path, game_object):
        self.bg = pygame.image.load("../graphics/decoration/background/bg1_back.png")
        self.game_object = game_object
        self.start_button = Button(settings.screen_width / 2 - (300 / 2), 170, 300, 130, "Старт",
                                   buttons_image_path)
        self.quit_button = Button(settings.screen_width / 2 - (300 / 2), 350, 300, 130, "Выход", buttons_image_path)

    # Функция отображения составляющих меню на экран
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(drawtext(settings.game_name, 70, "#FFFFFF"), (settings.screen_width // 2 - 250, 70))
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

        for event in pygame.event.get():
            self.start_button.event_control(event, pygame.mouse.get_pos())
            self.quit_button.event_control(event, pygame.mouse.get_pos())

            if event.type == pygame.USEREVENT and event.button == self.start_button:
                self.game_object.status = 'overworld'

            if event.type == pygame.USEREVENT and event.button == self.quit_button:
                pygame.quit()

# Класс для интерфейса окончания игры
class End:
    def __init__(self, buttons_image_path, game_object):
        self.bg = pygame.image.load('../graphics/decoration/background/bg1_back.png')
        self.game_object = game_object
        self.menu_button = Button(settings.screen_width / 2 - (300 / 2), 350, 300, 130, "Меню", buttons_image_path)
        self.coin = pygame.image.load("../graphics/ui/coin1.png")
        self.coin = pygame.transform.scale(self.coin, (64, 64))

    # Функция отображения конца игры на экран
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(drawtext("Вы выиграли!", 70, "#FFFFFF"), (settings.screen_width // 2 - 250, 70))
        screen.blit(drawtext("Вы собрали:", 40, "#FFFFFF"), (settings.screen_width // 2 - 120, 160))
        screen.blit(self.coin, (settings.screen_width // 2 - 70, 210))
        screen.blit(drawtext(f"{self.game_object.coins}", 40, "#FFD966"), (settings.screen_width // 2, 220))
        self.menu_button.draw(screen)

        for event in pygame.event.get():
            self.menu_button.event_control(event, pygame.mouse.get_pos())

            if event.type == pygame.USEREVENT and event.button == self.menu_button:
                self.game_object.status = "menu"
