import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个外星人的类'''
    def __init__(self, ai_set, screen):
        '''初始化外星人并且设置初始位置'''
        super().__init__()
        self.screen = screen
        self.ai_set = ai_set

        #加载外星人图像
        self.image = pygame.image.load('../images/alien.bmp')
        self.rect = self.image.get_rect()

        #每个外星人都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人的准确位置
        self.x = float(self.rect.x)
    def blitme(self):
        '''指定位置绘制外星人'''
        self.screen.blit(self.image,self.rect)

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_set.alien_speed_factor * self.ai_set.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



