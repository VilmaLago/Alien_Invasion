import pygame.font

from pygame.sprite import Group
from ship import Ship

class ScoreBoard():
    '''Classe com configurações dos scores do jogo.'''

    def __init__(self, ai_settings, screen, stats):
        '''Inicialize as configurações dos scores.'''
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.stats = stats

        # Defina a cor e a fonte do score.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare a imagem do painel de score.
        self.prep_score()

        # Prepare a imagem do high score.
        self.prep_high_score()

        # Prepare o nível do jogo.
        self.prep_level()

        # Prepare a quantidade de naves restantes.
        self.prep_ship()

    def prep_score(self):
        '''Transforme o score em uma imagem renderizada.'''
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_color,
            self.ai_settings.bg_color
        )

        # Mostre o score no canto superior direito da tela.
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def show_score(self):
        '''Mostre o score na tela.'''
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        '''Crie a imagem renderizada do high score.'''
        rounded_high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(rounded_high_score)
        # Crie a imagem do high score.
        self.high_score_image = self.font.render(
            high_score_str, 
            True, 
            self.text_color, 
            self.ai_settings.bg_color
        )
        self.high_score_rect = self.high_score_image.get_rect()
        
        # Posicione a imagem no centro superior da tela.
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_image_rect.top
        
    def prep_level(self):
        '''Crie a imagem renderizada do nível do jogo.'''
        self.level_image = self.font.render(
            str(self.stats.level), True,
            self.text_color, self.ai_settings.bg_color
        )
        # Configure a posição do nível abaixo do score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_image_rect.right
        self.level_rect.top = self.score_image_rect.bottom + 10

    def prep_ship(self):
        '''Mostre a quantidade de naves restantes como imagens na tela.'''
        self.ships = Group()
        # Para cada nave criada, desenhe-a na tela na posição configurada.
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.resize(20, 35)
            # Configure a posição de cada nave.
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # Adicione cada uma das naves no grupo.
            self.ships.add(ship)