import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

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

# 定义方块墙类
class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

    def draw(self):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))

# 定义坦克类
class Tank:
    def __init__(self, x, y, image, is_enemy=False):
        self.x = x
        self.y = y
        self.image = image
        self.speed = random.randint(3, 6)  # 随机速度
        self.bullets = []
        self.is_enemy = is_enemy  # 是否是敌方坦克
        self.direction = random.choice([0, 1, 2, 3])  # 随机初始方向
        self.attack_frequency = random.uniform(0.005, 0.02)  # 随机攻击频率

    def move(self, walls):
        if self.is_enemy:
            # 敌方坦克按照巡逻方式移动
            if self.direction == 0:  # 向右移动
                new_x = self.x + self.speed
                if not self.check_collision(new_x, self.y, walls):
                    self.x = new_x
                if self.x >= WIDTH - 40:
                    self.x = WIDTH - 40
                    self.direction = random.choice([1, 3])  # 随机转向下或上
            elif self.direction == 1:  # 向下移动
                new_y = self.y + self.speed
                if not self.check_collision(self.x, new_y, walls):
                    self.y = new_y
                if self.y >= HEIGHT - 40:
                    self.y = HEIGHT - 40
                    self.direction = random.choice([0, 2])  # 随机转向右或左
            elif self.direction == 2:  # 向左移动
                new_x = self.x - self.speed
                if not self.check_collision(new_x, self.y, walls):
                    self.x = new_x
                if self.x <= 0:
                    self.x = 0
                    self.direction = random.choice([1, 3])  # 随机转向下或上
            elif self.direction == 3:  # 向上移动
                new_y = self.y - self.speed
                if not self.check_collision(self.x, new_y, walls):
                    self.y = new_y
                if self.y <= 0:
                    self.y = 0
                    self.direction = random.choice([0, 2])  # 随机转向右或左
        else:
            # 玩家坦克移动逻辑
            keys = pygame.key.get_pressed()
            new_x, new_y = self.x, self.y
            if keys[pygame.K_LEFT]:
                new_x -= self.speed
            if keys[pygame.K_RIGHT]:
                new_x += self.speed
            if keys[pygame.K_UP]:
                new_y -= self.speed
            if keys[pygame.K_DOWN]:
                new_y += self.speed

            # 检测碰撞
            if not self.check_collision(new_x, new_y, walls):
                self.x = new_x
                self.y = new_y

            # 边界检测
            if self.x < 0:
                self.x = 0
            elif self.x > WIDTH - 40:
                self.x = WIDTH - 40
            if self.y < 0:
                self.y = 0
            elif self.y > HEIGHT - 40:
                self.y = HEIGHT - 40

    def check_collision(self, x, y, walls):
        # 检测坦克是否与墙碰撞
        for wall in walls:
            if (x < wall.x + wall.width and x + 40 > wall.x and
                y < wall.y + wall.height and y + 40 > wall.y):
                return True
        return False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def shoot(self):
        bullet = Bullet(self.x + 15, self.y, self.is_enemy)  # 子弹从坦克中心发射
        self.bullets.append(bullet)

# 定义子弹类
class Bullet:
    def __init__(self, x, y, is_enemy):
        self.x = x
        self.y = y
        self.speed = 10
        self.is_enemy = is_enemy  # 是否是敌方子弹

    def move(self, walls):
        if self.is_enemy:
            self.y += self.speed  # 敌方子弹向下移动
        else:
            self.y -= self.speed  # 玩家子弹向上移动

        # 检测子弹是否击中墙
        for wall in walls:
            if (self.x < wall.x + wall.width and self.x + 10 > wall.x and
                self.y < wall.y + wall.height and self.y + 20 > wall.y):
                return True  # 子弹击中墙
        return False

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# 创建玩家坦克
player_tank = Tank(WIDTH // 2, HEIGHT - 60, player_tank_image)

# 创建敌方坦克列表
enemy_tanks = []
for _ in range(5):
    enemy_tank = Tank(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT // 2), enemy_tank_image, is_enemy=True)
    enemy_tanks.append(enemy_tank)

# 创建方块墙列表
walls = []
for _ in range(10):  # 生成10个方块墙
    wall = Wall(random.randint(0, WIDTH // 40 - 1) * 40, random.randint(0, HEIGHT // 40 - 1) * 40)
    walls.append(wall)

# 游戏主循环
running = True
game_over = False
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
    player_tank.move(walls)

    # 绘制玩家坦克
    player_tank.draw()

    # 处理玩家子弹
    for bullet in player_tank.bullets[:]:
        bullet.move(walls)
        bullet.draw()

        # 移除屏幕外的子弹或击中墙的子弹
        if bullet.y < 0 or bullet.y > HEIGHT or bullet.move(walls):
            player_tank.bullets.remove(bullet)

        # 检测玩家子弹是否击中敌方坦克
        for enemy_tank in enemy_tanks[:]:
            if (bullet.x < enemy_tank.x + 40 and bullet.x + 10 > enemy_tank.x and
                bullet.y < enemy_tank.y + 40 and bullet.y + 20 > enemy_tank.y):
                player_tank.bullets.remove(bullet)
                enemy_tanks.remove(enemy_tank)
                break

    # 处理敌方坦克
    for enemy_tank in enemy_tanks:
        # 敌方坦克按照巡逻方式移动
        enemy_tank.move(walls)

        # 敌方坦克随机发射子弹
        if random.random() < enemy_tank.attack_frequency:  # 根据攻击频率发射子弹
            enemy_tank.shoot()

        # 检测敌方坦克是否与玩家坦克碰撞
        if (enemy_tank.x < player_tank.x + 40 and enemy_tank.x + 40 > player_tank.x and
            enemy_tank.y < player_tank.y + 40 and enemy_tank.y + 40 > player_tank.y):
            game_over = True

        # 绘制敌方坦克
        enemy_tank.draw()

        # 处理敌方子弹
        for bullet in enemy_tank.bullets[:]:
            bullet.move(walls)
            bullet.draw()

            # 移除屏幕外的子弹或击中墙的子弹
            if bullet.y < 0 or bullet.y > HEIGHT or bullet.move(walls):
                enemy_tank.bullets.remove(bullet)

            # 检测敌方子弹是否击中玩家坦克
            if (bullet.x < player_tank.x + 40 and bullet.x + 10 > player_tank.x and
                bullet.y < player_tank.y + 40 and bullet.y + 20 > player_tank.y):
                game_over = True

    # 绘制方块墙
    for wall in walls:
        wall.draw()

    # 游戏结束处理
    if game_over:
        font = pygame.font.SysFont(None, 74)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)  # 等待3秒后退出
        running = False

    # 更新显示
    pygame.display.flip()
    clock.tick(30)

# 退出游戏
pygame.quit()