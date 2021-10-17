# Crie uma classe para as balas.
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Classe que define as configuraçõs das balas da nave.'''

    def __init__(self, ai_settings, screen, ship):
        '''Crie um objeto bala na posição da nave.'''
        super(Bullet, self).__init__()
        self.screen = screen
    
        # Crie o rect da bala e depois configure sua posição.
        self.rect = pygame.Rect(
            0,
            0,
            ai_settings.bullet_width,
            ai_settings.bullet_height
            )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Guarde a posição da bala como um valor decimal.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Mova a bala para cima.'''
        # Atualize a posição decimal da bala.
        self.y -= self.speed_factor
        # Atualize a posição do rect.
        self.rect.y = self.y

    def draw_bullet(self):
        '''Desenhe a bala na tela.'''
        pygame.draw.rect(self.screen, self.color, self.rect)