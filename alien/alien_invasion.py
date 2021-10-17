import pygame

from pygame.sprite import Group 

from settings import Settings

from ship import Ship

import game_functions as gf

from game_stats import GameStats

from button import Button

from scoreboard import ScoreBoard

def run_game():
    # Inicialize o jogo e crie um objeto de cena.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Crie o botão iniciar de jogar.
    play_button = Button(ai_settings, screen, "Play")

    # Crie uma instância que inicialize estatísticas de jogo.
    # Crie a instância do score.
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Crie uma instância da nave, um grupo de balas e um de aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Crie uma frota de Aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Comece o main loop do jogo.
    while True:
        gf.check_events(
            ai_settings, stats, screen, ship, 
            sb, aliens, bullets, play_button)

        if stats.game_active:
            ship.update()
            gf.update_bullets(
                ai_settings, stats, screen, sb,
                 ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets)

        # Atualize a tela ao longo de cada loop.
        gf.update_screen(
            ai_settings, stats, screen, ship, 
            sb, aliens, bullets, play_button)

run_game()