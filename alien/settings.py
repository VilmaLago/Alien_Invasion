class Settings():
    '''Crie uma classe com as configurações do jogo.'''
    
    def __init__(self):
        '''Inicie as configurações estáticas do jogo.'''
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (
            0, 
            0, 
            10 
        )
        # Configurações da nave.
        self.ship_limit = 3

        # Configurações das balas.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (
            255,
            255,
            255
        )
        self.bullets_allowed = 3

        # Configurações do Alien
        self.fleet_drop_speed = 10

        # Quão rápido o jogo acelera.
        self.speedup_factor = 1.1

        # Quanto aumenta os pontos dos aliens>
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        '''Inicialize os atributos que mudam ao longo do jogo.'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 2
        
        # A Fleet Direction de 1 é para a direita, enquanto -1 é esquerda.
        self.fleet_direction = 1

        # Pontos por cada alien destruído.
        self.alien_points = 50

    def increase_speed(self):
        '''Acelere as velocidades dinâmicas do jogo.'''
        self.alien_speed_factor *= self.speedup_factor
        self.bullet_speed_factor *= self.speedup_factor
        self.ship_speed_factor *= self.speedup_factor

        self.alien_points = int(self.alien_points * self.score_scale)