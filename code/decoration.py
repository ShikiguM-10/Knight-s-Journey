import pygame
from settings import screen_width, screen_height


class Background:
    def __init__(self):
        self.background_img = pygame.image.load('../graphics/decoration/background/fair.png').convert()
        self.background_img = pygame.transform.scale(self.background_img,
                                                     (screen_width, screen_height))

    # Отрисовываем задний фон
    def draw(self, surface):
        my_rect = (0, 0, screen_width, screen_height)
        surface.blit(self.background_img, my_rect)
