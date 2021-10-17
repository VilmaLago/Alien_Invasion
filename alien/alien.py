# Crie uma classe Alien
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Crie uma classe de Aliens.'''

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carregue a imagem do Alien.
        # Configure seus atributos.
        self.image = pygame.transform.scale(
            pygame.image.load('images/alien.png'),
            (100, 50)
        )
        self.rect = self.image.get_rect()
        
        # Configure a posição do Alien ao aparecer na tela.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Guarde a posição exata do Alien.
        self.x = float(self.rect.x)
    
    def blitme(self):
        '''Desenhe o Alien na tela.'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''Mova os aliens para a direita ou esquerda
        de acordo com sua velocidade.'''
        self.x += (self.ai_settings.alien_speed_factor * 
        self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Retorne True caso o alien atinja as bordas da tela.'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True