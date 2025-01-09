import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定义屏幕大小和方块大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("超级玛丽")

# 定义时钟
clock = pygame.time.Clock()

# 定义字体
font = pygame.font.SysFont(None, 35)

# 定义玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_SIZE
        self.rect.y = SCREEN_HEIGHT - 2 * BLOCK_SIZE
        self.change_x = 0
        self.change_y = 0
        self.jumping = False

    def update(self):
        # 重力
        self.calc_grav()

        # 移动左右
        self.rect.x += self.change_x

        # 检查是否碰到墙壁
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # 移动上下
        self.rect.y += self.change_y

        # 检查是否碰到墙壁
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

# 定义平台类
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

# 定义关卡类
class Level:
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)

# 定义第一关
class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        level = [
            [210, 70, 500, 500],
            [210, 70, 200, 400],
            [210, 70, 600, 300],
        ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

# 主游戏循环
def main():
    player = Player()
    level_list = [Level_01(player)]
    current_level_no = 0
    current_level = level_list[current_level_no]
    player.level = current_level

    active_sprite_list = pygame.sprite.Group()
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        active_sprite_list.update()
        current_level.update()

        if player.rect.right >= SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.left <= 0:
            player.rect.left = 0

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()