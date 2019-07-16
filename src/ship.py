import pygame
class Ship():
    def __init__(self, screen, ai_set):
        '''初始化飞船并初始化器位置'''
        self.screen = screen
        self.ai_set = ai_set
        #加载飞船图像并获取其外形
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #把飞机放在屏幕最下方
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 飞船的属性中存储小数
        self.center = float(self.rect.centerx)
        #移动标志位
        self.moving_right = False
        self.moving_left = False
    def update(self):
        '''根据移动标志调整飞船位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_set.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_set.ship_speed_factor
        #根据self.center更新rect对象
        self.rect.centerx = self.center


    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)


