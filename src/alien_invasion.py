import pygame
from pygame.sprite import Group

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
    ship = Ship(screen, ai_set)
    #创建一个编组存储子弹
    bullets = Group()

    #游戏主循环开始
    while True:
        #监控键盘和鼠标事件
        gf.check_events(ai_set, screen, ship, bullets)
        ship.update()
        bullets.update()
        gf.update_screen(ai_set, screen, ship, bullets)
        # screen.fill(ai_set.bg_color)
        # ship.blitme()
        # #显示最新绘制的屏幕
        # pygame.display.flip()


if __name__ == '__main__':
    run_game()