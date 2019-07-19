import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_play_button(status, play_button, mouse_x, mouse_y, ai_set, screen, ship, aliens, bullets, sb):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not status.game_active:
        # 重置游戏设置
        ai_set.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        status.reset_status()
        status.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_set, screen, ship, aliens)
        ship.center_ship()

def check_events(ai_set, screen, ship, bullets, status, play_button, aliens, sb):
    '''响应鼠标和键盘事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event,ai_set, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(status, play_button, mouse_x, mouse_y, ai_set, screen, ship, aliens, bullets, sb)

def check_key_down_events(event,ai_set, screen,  ship, bullets):
    '''按键响应'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_set, screen,  ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_key_up_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_set, screen, ship, aliens, bullets, play_button, status, sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都要重绘屏幕
    screen.fill(ai_set.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not status.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_set, screen, ship, aliens, bullets, status, sb):
    '''更新子弹的位置，并且删除消失的子弹'''
    bullets.update()
    '''删除消失的子弹'''
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_set, screen, ship, aliens, bullets, status, sb)


def fire_bullet(ai_set, screen,  ship, bullets):
    if len(bullets) <= ai_set.bullet_allowed:
        new_bullet = Bullet(ai_set, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_set, screen, ship, aliens):
    '''创建外星人群组'''
    #创建一个外星人，并计算可以容纳外星人个数
    #外星人间距为外星人个数
    alien = Alien(ai_set, screen)
    number_aliens_x = get_number_aliens_x(ai_set, alien.rect.width)
    number_rows = get_number_rows(ai_set, ship.rect.height,alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人，并且加入当前行
            create_alien(ai_set, screen, aliens, alien_number,row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_set, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_set, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_set, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_set.screen_height -(3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def check_fleet_edges(ai_set, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_set, aliens)
            break

def change_fleet_direction(ai_set, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_set.fleet_drop_speed
    ai_set.fleet_direction *= -1


def check_aliens_bottom(ai_set, status, screen, ship, aliens, bullets, sb):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(aliens, ai_set, ship, status, bullets, screen, sb)
            break


def update_aliens(aliens, ai_set, ship, status, bullets, screen,sb):
    """检查是否有外星人位于屏幕边缘,更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_set, aliens)
    aliens.update()
    #检查外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(aliens, ai_set, ship, status, bullets, screen,sb)
    #检查外星人是否到达底部
    check_aliens_bottom(ai_set, status, screen, ship, aliens, bullets,sb)

def check_bullet_alien_collisions(ai_set, screen, ship, aliens, bullets,status, sb):
    '''
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    '''
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            status.score += ai_set.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(status, sb)

    if len(aliens) == 0:
        # 删除现有的所有子弹，并创建一个新的外星人群
        bullets.empty()
        ai_set.increase_speed()
        # 提高等级
        status.level += 1
        sb.prep_level()
        create_fleet(ai_set, screen, ship, aliens)


def ship_hit(aliens, ai_set, ship, status, bullets, screen, sb):
    '''响应被外星人撞到的飞船'''
    #将ships_left -=1
    # print(status.ships_left)
    if status.ships_left > 0:
        status.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_set, screen, ship, aliens)
        ship.center_ship()
        #暂停1秒
        sleep(1)
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


