import pygame
import random

# ゲームの初期設定
pygame.init()
WIDTH, HEIGHT = 600, 800  # 縦長画面のサイズ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# ゲームの設定
paddle_width = 100
paddle_height = 15
ball_radius = 10
block_width = 70
block_height = 25
block_rows = 5
block_cols = 6
block_gap = 7
block_y_offset = 100

font = pygame.font.SysFont("Arial", 30)

# 初期スピードの設定
initial_ball_speed_x = 5
initial_ball_speed_y = -5
max_speed_x = initial_ball_speed_x * 1.45  # 初期スピードの1.45倍を上限とする
max_speed_y = initial_ball_speed_y * 1.45

def show_start_screen():
    """スタート画面を表示する関数"""
    screen.fill(BLACK)
    title_text = font.render("Press any key to start", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def initialize_game():
    """ゲームの初期化を行う関数"""
    global paddle_x, paddle_y, paddle_speed
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global blocks, score
    
    # パドルの設定
    paddle_x = (WIDTH - paddle_width) // 2
    paddle_y = HEIGHT - paddle_height - 30
    paddle_speed = 10

    # ボールの設定
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = initial_ball_speed_x * random.choice((1, -1))
    ball_speed_y = initial_ball_speed_y

    # ブロックの設定
    blocks = [(x * (block_width + block_gap) + (WIDTH - (block_cols * (block_width + block_gap))) // 2,
                block_y_offset + y * (block_height + block_gap)) 
              for y in range(block_rows) for x in range(block_cols)]

    # スコアの初期化
    score = 0

def show_result_screen(score):
    """リザルト画面を表示する関数"""
    screen.fill(BLACK)
    rank = ""
    if score >= 280:
        rank = "A"
    elif score >= 120:
        rank = "B"
    elif score >= 100:
        rank = "C"
    else:
        rank = "D"

    score_text = font.render(f"Score: {score}", True, WHITE)
    rank_text = font.render(f"Rank: {rank}", True, WHITE)
    restart_text = font.render("Press any key to restart", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def run_game():
    """ゲームを実行するメインループ"""
    global paddle_x, paddle_y, paddle_speed
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global blocks, score
    
    initialize_game()
    running = True
    while running:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # キー入力処理
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed

        # パドルの移動制限
        if paddle_x < 0:
            paddle_x = 0
        elif paddle_x > WIDTH - paddle_width:
            paddle_x = WIDTH - paddle_width

        # ボールの移動
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 壁でのボールの反射
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_speed_x *= -1
        if ball_y <= 0:
            ball_speed_y *= -1
        if ball_y >= HEIGHT:
            running = False  # ゲームオーバー

        # パドルとの衝突
        if (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height) and (paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_speed_y *= -1
            paddle_speed *= 1.1

        # ブロックとの衝突
        for block in blocks[:]:
            block_rect = pygame.Rect(block[0], block[1], block_width, block_height)
            if block_rect.collidepoint(ball_x, ball_y):
                # ブロックのどの辺に当たったかを確認して反射を調整
                if abs(ball_y - block_rect.top) < ball_radius and ball_speed_y > 0:
                    ball_speed_y *= -1  # 上側で衝突
                elif abs(ball_y - block_rect.bottom) < ball_radius and ball_speed_y < 0:
                    ball_speed_y *= -1  # 下側で衝突
                elif abs(ball_x - block_rect.left) < ball_radius and ball_speed_x > 0:
                    ball_speed_x *= -1  # 左側で衝突
                elif abs(ball_x - block_rect.right) < ball_radius and ball_speed_x < 0:
                    ball_speed_x *= -1  # 右側で衝突

                blocks.remove(block)
                
                # スピードの上昇と上限の設定
                #ball_speed_x = min(ball_speed_x * 1.1, max_speed_x)
                #ball_speed_y = min(ball_speed_y * 1.1, max_speed_y)
                
                score += 10

        # 描画処理
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        for block in blocks:
            pygame.draw.rect(screen, WHITE, (block[0], block[1], block_width, block_height))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

# メインループ
while True:
    show_start_screen()
    run_game()
    show_result_screen(score)
