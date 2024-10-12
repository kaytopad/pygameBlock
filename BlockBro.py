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

# パドルの設定
paddle_width = 100
paddle_height = 15
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 30  # パドルを少し上げる
paddle_speed = 10  # パドルの移動速度

# ボールの設定
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = -5

# ブロックの設定
block_width = 70  # ブロックの幅
block_height = 20  # ブロックの高さ
block_rows = 6  # 行の数（4行）
block_cols = 6  # 列の数（7列）
block_gap = 5  # ブロック間の隙間
block_y_offset = 120  # スコアの上に隙間を作る

# 中央揃えのブロック座標計算
blocks = [(x * (block_width + block_gap) + (WIDTH - (block_cols * (block_width + block_gap))) // 2,
            block_y_offset + y * (block_height + block_gap)) 
          for y in range(block_rows) for x in range(block_cols)]

# スコアの設定
score = 0
font = pygame.font.SysFont("Arial", 30)

# メインゲームループ
running = True
while running:
    pygame.time.delay(30)  # フレームレートの制御

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キーボード入力によるパドルの移動
    keys = pygame.key.get_pressed()  # 現在押されているキーを取得
    if keys[pygame.K_LEFT]:  # 左キーが押されている場合
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:  # 右キーが押されている場合
        paddle_x += paddle_speed

    # パドルの境界を制限
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > WIDTH - paddle_width:
        paddle_x = WIDTH - paddle_width

    # ボールの移動
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # ボールの反射処理
    if ball_x <= 0 or ball_x >= WIDTH:
        ball_speed_x *= -1  # 左右の壁で反射
    if ball_y <= 0:
        ball_speed_y *= -1  # 上の壁で反射
    if ball_y >= HEIGHT:
        running = False  # 下の壁に当たったらゲームオーバー

    # ボールとパドルの衝突判定
    if (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height) and (paddle_x <= ball_x <= paddle_x + paddle_width):
        ball_speed_y *= -1  # パドルに当たったら反射
        paddle_speed *= 1.1  # パドルの速度を10%増加

    # ボールとブロックの衝突判定
    for block in blocks[:]:
        block_rect = pygame.Rect(block[0], block[1], block_width, block_height)
        if block_rect.collidepoint(ball_x, ball_y):
            ball_speed_y *= -1  # ブロックに当たったら反射
            blocks.remove(block)  # ブロックを削除
            ball_speed_x *= 1.1  # 当たったらX軸の速度を10%増加
            ball_speed_y *= 1.1  # 当たったらY軸の速度を10%増加
            score += 10  # スコアを加算

    # 描画処理
    screen.fill(BLACK)  # 背景の塗りつぶし
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))  # パドルの描画
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)  # ボールの描画

    # ブロックの描画
    for block in blocks:
        pygame.draw.rect(screen, WHITE, (block[0], block[1], block_width, block_height))

    # スコアの表示
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))  # スコアを左上に表示

    pygame.display.flip()  # 画面を更新

pygame.quit()
