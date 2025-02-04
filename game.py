import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 遊戲窗口大小
WIDTH = 800
HEIGHT = 600

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 蛇身和食物大小
CELL_SIZE = 20

# 初始化窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("貪食蛇遊戲")

# 遊戲時鐘
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.body = [self.head.copy(),
                     [self.head[0] - CELL_SIZE, self.head[1]],
                     [self.head[0] - 2 * CELL_SIZE, self.head[1]]]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"

    def change_direction(self, new_dir):
        if (self.direction, new_dir) not in [("LEFT", "RIGHT"), ("RIGHT", "LEFT"),
                                             ("UP", "DOWN"), ("DOWN", "UP")]:
            self.direction = new_dir

    def move(self):
        # 更新頭部位置
        if self.direction == "RIGHT":
            self.head[0] += CELL_SIZE
        elif self.direction == "LEFT":
            self.head[0] -= CELL_SIZE
        elif self.direction == "UP":
            self.head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            self.head[1] += CELL_SIZE

        # 插入新的頭部，移除尾部（如果沒有吃到食物）
        self.body.insert(0, self.head.copy())
        if not game.food_eaten:
            self.body.pop()
        else:
            game.food_eaten = False


class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        while True:
            x = random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE)
            y = random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE)
            if [x, y] not in snake.body:
                return [x, y]


class Game:
    def __init__(self):
        self.score = 0
        self.food = Food()
        self.food_eaten = False
        self.game_over = False
        self.speed = 10  # 初始速度

    def check_collision(self):
        # 邊界檢測
        if (snake.head[0] < 0 or snake.head[0] >= WIDTH or
                snake.head[1] < 0 or snake.head[1] >= HEIGHT):
            return True

        # 自我碰撞檢測
        if snake.head in snake.body[1:]:
            return True

        return False

    def check_food(self):
        if snake.head == self.food.position:
            self.score += 100
            self.food = Food()
            self.food_eaten = True
            self.speed += 1  # 每次吃到食物，速度增加 1


def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# 創建遊戲對象
snake = Snake()
game = Game()

# 主遊戲循環
while True:
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_r and game.game_over:
                # 重置遊戲
                snake = Snake()
                game = Game()

    if not game.game_over:
        # 移動蛇
        snake.move()

        # 檢查碰撞
        if game.check_collision():
            game.game_over = True

        # 檢查是否吃到食物
        game.check_food()

    # 繪製畫面
    screen.fill(BLACK)

    # 繪製蛇
    for idx, segment in enumerate(snake.body):
        color = GREEN if idx == 0 else WHITE
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1))

    # 繪製食物
    pygame.draw.rect(screen, RED, (game.food.position[0], game.food.position[1], CELL_SIZE - 1, CELL_SIZE - 1))

    # 顯示分數和速度
    draw_text(f"Score: {game.score}", 24, WHITE, WIDTH // 2, 20)
    draw_text(f"Speed: {game.speed}", 24, WHITE, WIDTH // 2, 50)

    if game.game_over:
        draw_text("Game Over! Press R to restart", 48, RED, WIDTH // 2, HEIGHT // 2)

    # 更新畫面
    pygame.display.flip()

    # 控制遊戲速度
    clock.tick(game.speed)
