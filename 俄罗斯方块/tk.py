import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 定义屏幕大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克大战")

# 定义时钟
clock = pygame.time.Clock()

# 创建简单的坦克图形
player_tank_image = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.rect(player_tank_image, GREEN, (10, 10, 20, 20))  # 坦克车身
pygame.draw.rect(player_tank_image, GREEN, (18, 0, 4, 10))    # 坦克炮管

enemy_tank_image = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.rect(enemy_tank_image, RED, (10, 10, 20, 20))     # 敌方坦克车身
pygame.draw.rect(enemy_tank_image, RED, (18, 0, 4, 10))       # 敌方坦克炮管

# 定义坦克类
class Tank:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed = 5
        self.bullets = []

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def shoot(self):
        bullet = Bullet(self.x + 15, self.y)  # 子弹从坦克中心发射
        self.bullets.append(bullet)

# 定义子弹类
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed  # 子弹向上移动

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# 创建玩家坦克
player_tank = Tank(WIDTH // 2, HEIGHT - 60, player_tank_image)

# 创建敌方坦克列表
enemy_tanks = []
for _ in range(5):
    enemy_tank = Tank(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT // 2), enemy_tank_image)
    enemy_tanks.append(enemy_tank)

# 游戏主循环
running = True
while running:
    screen.fill(BLACK)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_tank.shoot()

    # 处理玩家坦克移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_tank.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player_tank.move(1, 0)
    if keys[pygame.K_UP]:
        player_tank.move(0, -1)
    if keys[pygame.K_DOWN]:
        player_tank.move(0, 1)

    # 绘制玩家坦克
    player_tank.draw()

    # 处理玩家子弹
    for bullet in player_tank.bullets[:]:
        bullet.move()
        bullet.draw()

        # 移除屏幕外的子弹
        if bullet.y < 0:
            player_tank.bullets.remove(bullet)

        # 检测子弹是否击中敌方坦克
        for enemy_tank in enemy_tanks[:]:
            if (bullet.x < enemy_tank.x + 40 and bullet.x + 10 > enemy_tank.x and
                bullet.y < enemy_tank.y + 40 and bullet.y + 20 > enemy_tank.y):
                player_tank.bullets.remove(bullet)
                enemy_tanks.remove(enemy_tank)
                break

    # 绘制敌方坦克
    for enemy_tank in enemy_tanks:
        enemy_tank.draw()

    # 更新显示
    pygame.display.flip()
    clock.tick(30)

# 退出游戏
pygame.quit()