import pygame


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, button_path):
        self.font = pygame.font.Font('../graphics/ui/font.ttf', 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.button_image = pygame.image.load(button_path)
        self.button_image = pygame.transform.scale(self.button_image, (width, height))

        self.rect = self.button_image.get_rect(topleft=(x, y))

    # Функция для прорисовки кнопки на экране и назначения для неё функций
    def draw(self, screen):
        screen.blit(self.button_image, self.rect.topleft)
        text = self.font.render(self.text, True, "black")
        text_coords = text.get_rect(center=self.rect.center)
        screen.blit(text, text_coords)

    def event_control(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos):
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
