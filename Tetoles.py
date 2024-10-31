import pygame
import random

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 300
screen_height = 600
block_size = 30

# Pygameのウィンドウを作成
screen = pygame.display.set_mode((screen_width + 150, screen_height)) # 次のテトリミノ表示用に横幅を拡張
pygame.display.set_caption('Tetris')

# 色の設定
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255)
]

# テトリミノの形状リスト
shapes = [
    [[1, 1, 1, 1]],
    [[2, 0, 0], [2, 2, 2]],
    [[0, 0, 3], [3, 3, 3]],
    [[4, 4], [4, 4]],
    [[0, 5, 5], [5, 5, 0]],
    [[6, 6, 6], [0, 6, 0]],
    [[7, 7, 0], [0, 7, 7]]
]

board_width = screen_width // block_size
board_height = screen_height // block_size
board = [[0] * board_width for _ in range(board_height)]

# スコアとレベル
score = 0
level = 1
lines_cleared = 0

# ポーズフラグ
is_paused = False

def create_tetromino():
    shape = random.choice(shapes)
    color = random.randint(1, len(colors) - 1)
    return {'shape': shape, 'color': color, 'x': board_width // 2 - len(shape[0]) // 2, 'y': 0}

def rotate_tetromino(tetromino):
    # 90度回転する関数
    rotated_shape = [list(row) for row in zip(*reversed(tetromino['shape']))]
    original_shape = tetromino['shape']
    tetromino['shape'] = rotated_shape
    if check_collision(tetromino):  # 衝突があれば回転を元に戻す
        tetromino['shape'] = original_shape

def draw_board():
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x] != 0:
                pygame.draw.rect(screen, colors[board[y][x]],
                                 (x * block_size, y * block_size, block_size, block_size))

def draw_tetromino(tetromino):
    shape = tetromino['shape']
    color = tetromino['color']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[color],
                                 ((tetromino['x'] + j) * block_size, 
                                  (tetromino['y'] + i) * block_size, block_size, block_size))

def draw_ghost_tetromino(tetromino):
    # ゴーストテトリミノの描画
    ghost = tetromino.copy()
    while not check_collision(ghost):
        ghost['y'] += 1
    ghost['y'] -= 1  # 衝突する直前の位置に戻す

    shape = ghost['shape']
    color = ghost['color']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[color],
                                 ((ghost['x'] + j) * block_size, 
                                  (ghost['y'] + i) * block_size, block_size, block_size), 1) # 枠線のみ描画

def move_tetromino(tetromino, dx, dy):
    tetromino['x'] += dx
    tetromino['y'] += dy

def check_collision(tetromino):
    shape = tetromino['shape']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                x = tetromino['x'] + j
                y = tetromino['y'] + i
                if x < 0 or x >= board_width or y >= board_height or board[y][x] != 0:
                    return True
    return False

def lock_tetromino(tetromino):
    shape = tetromino['shape']
    color = tetromino['color']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                board[tetromino['y'] + i][tetromino['x'] + j] = color

def clear_lines():
    global board, score, lines_cleared, level
    lines_to_clear = [i for i, row in enumerate(board) if all(row)]
    for i in lines_to_clear:
        del board[i]
        board.insert(0, [0] * board_width)
    # スコアとレベルの更新
    lines_cleared += len(lines_to_clear)
    score += 100 * len(lines_to_clear) * level
    if lines_cleared >= 10:
        level += 1
        lines_cleared -= 10

# 次のテトリミノ
next_tetromino = create_tetromino()

# メインループ
running = True
current_tetromino = create_tetromino()

while running:
    screen.fill((0, 0, 0))  # 背景を黒でクリア
    draw_board()
    draw_tetromino(current_tetromino)
    draw_ghost_tetromino(current_tetromino)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # スペースキーでポーズの切り替え
                is_paused = not is_paused
            if not is_paused:
                if event.key == pygame.K_LEFT:
                    move_tetromino(current_tetromino, -1, 0)
                    if check_collision(current_tetromino):
                        move_tetromino(current_tetromino, 1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_tetromino(current_tetromino, 1, 0)
                    if check_collision(current_tetromino):
                        move_tetromino(current_tetromino, -1, 0)
                elif event.key == pygame.K_DOWN:
                    move_tetromino(current_tetromino, 0, 1)
                    if check_collision(current_tetromino):
                        move_tetromino(current_tetromino, 0, -1)
                        lock_tetromino(current_tetromino)
                        current_tetromino = create_tetromino()
                        clear_lines()
                elif event.key == pygame.K_UP:
                    rotate_tetromino(current_tetromino)

    # ポーズ中でなければ画面を更新
    if not is_paused:
        pygame.display.update()

pygame.quit()
