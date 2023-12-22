import pygame

def drawtext(text, size, color):

    Font = pygame.font.Font("../graphics/ui/font.ttf", size)
    needtotype = Font.render(str(text), 0, color)

    return needtotype