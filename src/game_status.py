class GameStatus():
    '''跟踪游戏的统计信息'''
    def __init__(self, ai_set):
        '''初始化统计信息'''
        self.ai_set = ai_set
        self.reset_status()
        self.game_active = False
        # 在任何情况下都不应重置最高得分
        self.high_score = 0
    def reset_status(self):
        '''初始化游戏运行过程中可能变化的统计信息'''
        self.ships_left = self.ai_set.ship_limit
        self.score = 0
        self.level = 1
