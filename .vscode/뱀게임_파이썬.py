import pygame
import sys
import random

pygame.init()

# 화면 크기
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE  = (0, 128, 255)

# 화면 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# 뱀, 음식 초기화
snake1 = [(100, 100), (80, 100), (60, 100)]  # 사람(초록)
dir1 = (CELL_SIZE, 0)
snake2 = [(700, 700), (720, 700), (740, 700)]  # AI(파랑)
dir2 = (-CELL_SIZE, 0)
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

score1 = 0
score2 = 0

def draw_snake(snake, color):
    for pos in snake:
        pygame.draw.rect(screen, color, (*pos, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    return snake

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

def ai_direction(snake, food, current_dir):
    head = snake[0]
    fx, fy = food
    hx, hy = head
    # 우선순위: x축 정렬 → y축 정렬
    if fx > hx and current_dir != (-CELL_SIZE, 0):
        return (CELL_SIZE, 0)
    if fx < hx and current_dir != (CELL_SIZE, 0):
        return (-CELL_SIZE, 0)
    if fy > hy and current_dir != (0, -CELL_SIZE):
        return (0, CELL_SIZE)
    if fy < hy and current_dir != (0, CELL_SIZE):
        return (0, -CELL_SIZE)
    return current_dir

def snakes_collide(snake1, snake2):
    head1 = snake1[0]
    head2 = snake2[0]
    # 서로의 몸에 부딪히거나 머리가 겹치면 True
    if head1 in snake2 or head2 in snake1 or head1 == head2:
        return True
    return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dir1 != (0, CELL_SIZE):
                dir1 = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and dir1 != (0, -CELL_SIZE):
                dir1 = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and dir1 != (CELL_SIZE, 0):
                dir1 = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and dir1 != (-CELL_SIZE, 0):
                dir1 = (CELL_SIZE, 0)

    # AI 방향 결정
    dir2 = ai_direction(snake2, food, dir2)

    snake1 = move_snake(snake1, dir1)
    snake2 = move_snake(snake2, dir2)

    # 음식 먹었는지 확인
    ate1 = snake1[0] == food
    ate2 = snake2[0] == food

    #사칙연산을 calc 클래스로 구현



    if ate1 and ate2:
        # 동시에 먹으면 각자 점수 1점, 음식 새로 생성
        score1 += 1
        score2 += 1
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    elif ate1:
        score1 += 1
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    elif ate2:
        score2 += 1
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    else:
        snake1.pop()
        snake2.pop()

    # 충돌 체크
    if check_collision(snake1) or check_collision(snake2) or snakes_collide(snake1, snake2):
        break

    screen.fill(BLACK)
    draw_snake(snake1, GREEN)
    draw_snake(snake2, BLUE)
    draw_food(food)

    # 점수 표시
    font = pygame.font.SysFont('comicsans', 30)
    text1 = font.render(f'Player: {score1}', True, WHITE)
    text2 = font.render(f'AI: {score2}', True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (WIDTH - text2.get_width() - 10, 10))

    pygame.display.update()
    clock.tick(10)

# 게임 오버 메시지
font = pygame.font.SysFont('comicsans', 40)
if score1 > score2:
    msg = 'Player Wins!'
elif score2 > score1:
    msg = 'AI Wins!'
else:
    msg = 'Draw!'
text = font.render(f'Game Over - {msg}', True, WHITE)
screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()