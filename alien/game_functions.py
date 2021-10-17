import sys

import pygame

from bullet import Bullet

from alien import Alien 

from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Cheque os eventos com teclas pressionadas.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    '''Cheque os eventos quando as teclas forem soltas.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(
    ai_settings, stats, screen, ship,
    sb, aliens, bullets, play_button):
    '''Responda a eventos de teclado e mouse.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                stats,
                screen,
                ship,
                sb,
                aliens,
                bullets,
                play_button,
                mouse_x,
                mouse_y
            )

def check_play_button(
    ai_settings, stats, screen,
    ship, sb, aliens, bullets,
    play_button, mouse_x, mouse_y
    ):
    '''Ative o jogo se o botão inicial tiver sido clicado.'''
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:

        # Esconda o cursor.
        pygame.mouse.set_visible(False)

        # Resete as configurações dinâmicas.
        ai_settings.initialize_dynamic_settings()

        # Reinicie as configurações do jogo.
        stats.reset_stats()
        stats.game_active = True

        # Resete os scores e nível do jogo.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        # Reinicie a frota de aliens e remova balas velhas.
        aliens.empty()
        bullets.empty()

        # Crie uma nova frota alien e centralize a nave.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullets(ai_settings, screen, ship, bullets):
    '''Crie uma nova bala e armazene em bullets'''
    '''Apenas dentro do limite de balas permitido.'''
    # Crie uma nova bala e armazene ela no grupo bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
            
def update_screen(
    ai_settings, stats, screen, ship,
    sb, aliens, bullets, play_button):
    '''Atualize a visualização de tela.'''
    screen.fill(ai_settings.bg_color)

    # Redesenhe todas as balas entre nave e aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()

    # Desenhe cada alien do grupo aliens.
    aliens.draw(screen)

    # Mostre o scoreboard.
    sb.show_score()

    # Caso o jogo esteja inativo, desenhe o botão inicial.
    if not stats.game_active:
        play_button.draw_button()

    # Faça o mais recente desenho da tela visível.
    pygame.display.flip()

# Crie uma função para remover balas velhas.
def update_bullets(
    ai_settings, stats, screen, sb, 
    ship, aliens, bullets):
    '''Remova as balas que saírem da tela.'''
    # Atualize a lista de sprites do grupo bullets.
    bullets.update()
    # Remova as balas que alcançarem o topo da tela.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings,
        stats,
        screen,
        ship,
        sb,
        aliens,
        bullets
    )

def check_bullet_alien_collisions(
    ai_settings, stats, screen, ship, sb, 
    aliens, bullets):
    '''Responda a colisões entre balas e aliens.'''
    # Verifique se ouve colisões entre balas e aliens.
    # Se sim, livre-se de balas e aliens.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Aumente o score a cada alien destruído
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destrua balas ainda existentes e aumente as velocidades.
        bullets.empty()
        ai_settings.increase_speed()

        # Aumente o nível do jogo.
        stats.level += 1
        sb.prep_level()

        # Crie uma nova frota.
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    '''Atualize o valor do high score de acordo com o maior score alcançado.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def get_number_aliens_x(ai_settings, alien_width):
    '''Descubra quantos aliens cabem em uma linha.'''
    # Encontre a quantidade de aliens em uma linha.
    # O espaço entre dois aliens equivale à largura de um alien.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Defina quantas linhas de aliens cabem na tela.'''
    available_space_y = (
        ai_settings.screen_height -
        (3 * alien_height) -
        ship_height 
    )
    number_rows = int(available_space_y / (2 * alien_height)) 
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Crie um alien e adicione ele à linha.'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''Crie uma frota de aliens.'''
    # Crie um alien e encontre a quantidade de aliens em uma linha.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings,
        ship.rect.height,
        alien.rect.height
    )
    
    # Crie a primeira linha de aliens.
    # Reproduza a linha de acordo com a quantidade de linhas delimitadas.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(
                ai_settings, 
                screen, aliens, 
                alien_number, 
                row_number)

def check_fleet_edges(ai_settings, aliens):
    '''Cheque se algum alien alcançou a borda da tela.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            check_fleet_direction(ai_settings, aliens)
            break

def check_fleet_direction(ai_settings, aliens):
    '''Faça os aliens mudarem de direção 
    e descerem na tela caso algum tenha alcaçado a borda.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets):
    '''Responda a colisões entre aliens e nave.'''

    if stats.ship_left > 0:
        # Diminua o limite de naves disponível.
        stats.ship_left -= 1

        # Remova a frota ainda existente.
        # Remova as balas restantes.
        aliens.empty()
        bullets.empty()

        # Atualize a quantidade de naves restantes.
        sb.prep_ship()

        # Crie uma nova frota de aliens.
        # Centralize a nave.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Dê uma pausa.
        sleep(0.5)

        # Atualize a tela
        # update_screen(ai_settings, stats, screen, ship, aliens, bullets)

    else:
        stats.game_active = False
        # Mostre o cursor novamente.
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets):
    '''Se um alien tocar o canto inferior da tela, ship_hit.'''

    # Verifique se o alien tocou o canto inferior da tela.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        # Trate como se o alien tivesse acertado a nave.
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(
                ai_settings,
                stats,
                screen,
                ship,
                sb,
                aliens,
                bullets
            )
            break
    
def update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets):
    '''
    Cheque se algum alien alcançou as bordas da tela
    e atualize a posição de cada alien.'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Cheque por colisões entre alien e nave.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets)

    # Procure por aliens que tenham tocado o canto inferior da tela.
    check_aliens_bottom(
        ai_settings,
        stats,
        screen,
        ship,
        sb,
        aliens,
        bullets
    )