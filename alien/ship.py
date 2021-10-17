import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    '''Inicializar configurações da nave.'''

    def __init__(self, ai_settings, screen):
        '''Inicialize a nave e configure sua localização.'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carregue a imagem da nave.
        self.image = pygame.transform.scale(
            pygame.image.load('images/nave.png'),
            (80, 140)
        )
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Configure a posição da nave no centro inferior da tela.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Guarde um valor decimal para o eixo da nave.
        self.center = float(self.rect.centerx)

        # Flags de movimentação.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Se a flag de movimentação ativar, mexa a nave.'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # Aumente o valor do center, não do rect.
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Atualize o rect de acordo com o eixo center.
        self.rect.centerx = self.center

    # Carregue a imagem na posição configurada.
    def blitme(self):
        '''Carregar a imagem na posição configurada.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Centralize a nave na tela.'''
        self.center = self.screen_rect.centerx

    def resize(self, width, height):
        self.image = pygame.transform.scale(
            self.image,
            (width, height)
        )
        self.rect = self.image.get_rect()
