import pygame
from pygame.sprite import Group

from button import Button
from game_status import GameStatus
from scoreboard import Scoreboard
from src.setting import Setting
from ship import Ship
import game_function as gf


def run_game():
    '''初始化屏幕并创建一个屏幕对象'''
    pygame.init()
    ai_set = Setting()
    screen = pygame.display.set_mode((ai_set.screen_width,ai_set.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # bg_color = (230,230,230)
    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_set, screen)
    bullets = Group()
    aliens = Group()
    #创建外星人实例
    gf.create_fleet(ai_set, screen, ship, aliens)
    #创建一个用于存储游戏统计信息的实例
    status = GameStatus(ai_set)
    sb = Scoreboard(ai_set, screen, status)
    #创建play按钮
    play_button = Button(ai_set, screen, 'Play')
    #

    #游戏主循环开始
    while True:
        #监控键盘和鼠标事件
        gf.check_events(ai_set, screen, ship, bullets,status,play_button, aliens, sb)
        if status.game_active:
            ship.update()
            gf.update_bullets(ai_set, screen, ship, aliens, bullets, status, sb)
            gf.update_aliens(aliens, ai_set, ship, status, bullets, screen, sb)
        gf.update_screen(ai_set, screen, ship, aliens, bullets, play_button, status, sb)
        # screen.fill(ai_set.bg_color)
        # ship.blitme()
        # #显示最新绘制的屏幕
        # pygame.display.flip()



if __name__ == '__main__':
    run_game()