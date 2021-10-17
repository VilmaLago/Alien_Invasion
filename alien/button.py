import pygame.font

class Button():
    '''Crie uma classe para o botão inicial.'''

    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # Inicialize as configurações do botão
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.font_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Crie o botão e centralize-o na tela.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Coloque uma mensagem no botão
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''Configure a mensagem do botão,
        trsnforme-a em uma imagem e centralize na tela.'''
        self.msg_image = self.font.render(
            msg,
            True,
            self.font_color,
            self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center

    def draw_button(self):
        '''Desenhe o botão inicial na tela.'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)