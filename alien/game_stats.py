class GameStats():
    '''Classe para estatísticas do jogo.'''

    def __init__(self, ai_settings):
        '''Defina as estatísticas do jogo.'''
        self.ai_settings = ai_settings
        self.reset_stats()  
        # Comece Alien Invasion em um estado inativo.
        self.game_active = False
        # Defina o high score do jogo.
        self.high_score = 0

    def reset_stats(self):
        '''Inicialize estatísticas que vão mudar ao longo do jogo.'''
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1