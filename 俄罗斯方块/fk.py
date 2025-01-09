import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # 青色
    (255, 255, 0),  # 黄色
    (255, 165, 0),  # 橙色
    (0, 0, 255),    # 蓝色
    (0, 255, 0),    # 绿色
    (255, 0, 0),    # 红色
    (128, 0, 128)   # 紫色
]

# 定义方块大小和网格大小
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 定义屏幕大小
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 定义时钟
clock = pygame.time.Clock()

# 定义网格
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 定义当前方块和下一个方块
current_piece = None
next_piece = None

# 定义当前方块的位置
current_x = GRID_WIDTH // 2 - 1
current_y = 0

# 定义分数
score = 0

# 定义游戏结束标志
game_over = False

# 定义方块类
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 生成随机方块
def create_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return Piece(shape, color)

# 检查方块是否可以放置在指定位置
def can_place(piece, x, y):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return False
    return True

# 将方块放置在网格中
def place_piece(piece, x, y):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col]:
                grid[y + row][x + col] = piece.color

# 清除满行并更新分数
def clear_lines():
    global score
    lines_cleared = 0
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            del grid[row]
            grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    score += lines_cleared * 100

# 绘制网格
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[row][col] if grid[row][col] else GRAY,
                             (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 绘制当前方块
def draw_piece(piece, x, y):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col]:
                pygame.draw.rect(screen, piece.color,
                                 ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, BLACK,
                                 ((x + col) * BLOCK_SIZE, (y + row) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 主游戏循环
def main():
    global current_piece, next_piece, current_x, current_y, game_over, score

    current_piece = create_piece()
    next_piece = create_piece()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_place(current_piece, current_x - 1, current_y):
                        current_x -= 1
                if event.key == pygame.K_RIGHT:
                    if can_place(current_piece, current_x + 1, current_y):
                        current_x += 1
                if event.key == pygame.K_DOWN:
                    if can_place(current_piece, current_x, current_y + 1):
                        current_y += 1
                if event.key == pygame.K_UP:
                    rotated_piece = Piece(current_piece.shape, current_piece.color)
                    rotated_piece.rotate()
                    if can_place(rotated_piece, current_x, current_y):
                        current_piece.rotate()
                if event.key == pygame.K_SPACE:
                    while can_place(current_piece, current_x, current_y + 1):
                        current_y += 1

        if can_place(current_piece, current_x, current_y + 1):
            current_y += 1
        else:
            place_piece(current_piece, current_x, current_y)
            clear_lines()
            current_piece = next_piece
            next_piece = create_piece()
            current_x = GRID_WIDTH // 2 - 1
            current_y = 0
            if not can_place(current_piece, current_x, current_y):
                game_over = True

        screen.fill(BLACK)
        draw_grid()
        draw_piece(current_piece, current_x, current_y)
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()