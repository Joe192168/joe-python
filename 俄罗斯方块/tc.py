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
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 定义时钟
clock = pygame.time.Clock()

# 定义字体
font = pygame.font.SysFont(None, 35)

# 定义蛇的初始位置和速度
snake = [(100, 100), (80, 100), (60, 100)]
snake_direction = (BLOCK_SIZE, 0)

# 定义食物的初始位置
food = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

# 定义分数
score = 0

# 定义游戏结束标志
game_over = False

# 绘制蛇
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

# 绘制食物
def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

# 显示分数
def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# 主游戏循环
def main():
    global snake, snake_direction, food, score, game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, BLOCK_SIZE):
                    snake_direction = (0, -BLOCK_SIZE)
                if event.key == pygame.K_DOWN and snake_direction != (0, -BLOCK_SIZE):
                    snake_direction = (0, BLOCK_SIZE)
                if event.key == pygame.K_LEFT and snake_direction != (BLOCK_SIZE, 0):
                    snake_direction = (-BLOCK_SIZE, 0)
                if event.key == pygame.K_RIGHT and snake_direction != (-BLOCK_SIZE, 0):
                    snake_direction = (BLOCK_SIZE, 0)

        # 移动蛇
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # 检查是否吃到食物
        if snake[0] == food:
            score += 1
            food = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        else:
            snake.pop()

        # 检查是否撞墙或撞到自己
        if (snake[0][0] < 0 or snake[0][0] >= SCREEN_WIDTH or
            snake[0][1] < 0 or snake[0][1] >= SCREEN_HEIGHT or
            snake[0] in snake[1:]):
            game_over = True

        # 绘制屏幕
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        show_score(score)
        pygame.display.flip()

        # 控制游戏速度
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()