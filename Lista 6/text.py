import pygame, constants


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, constants.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)


class Button:
    def __init__(self, button_text, x, y, width, screen):
        self.text = button_text
        self.x = x
        self.y = y
        self.width = width
        self.screen = screen

    def draw(self):
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if self.check_click():
            button_text = pygame.font.Font(pygame.font.match_font('arial'), 18).render(self.text, True, 'black')
            pygame.draw.rect(self.screen, 'white', button_rect)
            pygame.draw.rect(self.screen, 'black', button_rect, 2)
        else:
            button_text = pygame.font.Font(pygame.font.match_font('arial'), 18).render(self.text, True, 'white')
            pygame.draw.rect(self.screen, 'black', button_rect)
            pygame.draw.rect(self.screen, 'white', button_rect, 2)
        self.screen.blit(button_text, (self.x + 7, self.y + 7))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False
