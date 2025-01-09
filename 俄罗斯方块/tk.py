import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定义屏幕大小和方块大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("坦克大战")

# 定义时钟
clock = pygame.time.Clock()

# 定义字体
font = pygame.font.SysFont(None, 35)

# 定义坦克类
class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 'up'
        self.speed = 2

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

    def change_direction(self, direction):
        self.direction = direction

# 定义子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 5

    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()

# 定义玩家和敌人
player = Tank(GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT - BLOCK_SIZE)
enemy = Tank(RED, SCREEN_WIDTH // 2, BLOCK_SIZE)

# 定义精灵组
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

bullets = pygame.sprite.Group()

# 定义分数
score = 0

# 定义游戏结束标志
game_over = False

# 主游戏循环
def main():
    global score, game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.change_direction('up')
                if event.key == pygame.K_DOWN:
                    player.change_direction('down')
                if event.key == pygame.K_LEFT:
                    player.change_direction('left')
                if event.key == pygame.K_RIGHT:
                    player.change_direction('right')
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.x + BLOCK_SIZE // 2 - 5, player.rect.y + BLOCK_SIZE // 2 - 5, player.direction)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # 更新精灵
        all_sprites.update()

        # 检查子弹是否击中敌人
        for bullet in bullets:
            if pygame.sprite.collide_rect(bullet, enemy):
                enemy.kill()
                bullet.kill()
                score += 1
                enemy = Tank(RED, random.randint(0, SCREEN_WIDTH - BLOCK_SIZE), random.randint(0, SCREEN_HEIGHT - BLOCK_SIZE))
                all_sprites.add(enemy)

        # 绘制屏幕
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        # 控制游戏速度
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()