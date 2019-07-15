import sys
import pygame
from src.setting import Setting
from ship import Ship


def run_game():
    '''初始化屏幕并创建一个屏幕对象'''
    pygame.init()
    ai_set = Setting()
    screen = pygame.display.set_mode((ai_set.screen_height,ai_set.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # bg_color = (230,230,230)
    ship = Ship(screen)

    #游戏主循环开始
    while True:
        #监控键盘和鼠标事件
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
        screen.fill(ai_set.bg_color)
        ship.blitme()
        #显示最新绘制的屏幕
        pygame.display.flip()


if __name__ == '__main__':
    run_game()