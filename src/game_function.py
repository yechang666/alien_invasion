import sys
import pygame
from bullet import Bullet

def check_events(ai_set, screen, ship, bullets):
    '''响应鼠标和键盘事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_events(event,ai_set, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_key_up_events(event, ship)

def check_key_down_events(event,ai_set, screen,  ship, bullets):
    '''按键响应'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_set,screen, ship)
        bullets.add(new_bullet)

def check_key_up_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(ai_set, screen, ship, bullets):
    '''更新屏幕上的图像，并切换到新屏幕'''
    #每次循环时都要重绘屏幕
    screen.fill(ai_set.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    pygame.display.flip()