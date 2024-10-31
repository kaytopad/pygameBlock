import pygame
import random

# Pygameの初期化
pygame.init()

# 画面サイズの設定（24ブロック幅×18ブロック高さ）
block_size = 24  # 各ブロックのサイズ
screen_width = block_size * 18
screen_height = block_size * 24

# Pygameのウィンドウを作成
screen = pygame.display.set_mode((screen_width, screen_height))
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
    [[1, 1, 1, 1]],  # I
    [[2, 2, 2], [2, 0, 0]],  # J
    [[0, 0, 3], [3, 3, 3]],  # L
    [[4, 4], [4, 4]],  # O
    [[5, 5, 0], [0, 5, 5]],  # S
    [[0, 6, 0], [6, 6, 6]],  # T
    [[7, 7, 0], [0, 7, 7]]   # Z
]

# ボードの幅と高さ
board_width = screen_width // block_size
board_height = screen_height // block_size
board = [[0] * board_width for _ in range(board_height)]

# スコアの初期化
score = 0

# テトリミノの生成
def create_tetromino():
    shape = random.choice(shapes)
    color = random.randint(1, len(colors) - 1)
    return {'shape': shape, 'color': color, 'x': board_width // 2 - len(shape[0]) // 2, 'y': 0}

# テトリミノの回転
def rotate_tetromino(tetromino):
    rotated_shape = [list(row) for row in zip(*reversed(tetromino['shape']))]
    original_shape = tetromino['shape']
    tetromino['shape'] = rotated_shape
    if check_collision(tetromino):
        tetromino['shape'] = original_shape

# テトリミノとボードの衝突判定
def check_collision(tetromino):
    shape = tetromino['shape']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                x = tetromino['x'] + j
                y = tetromino['y'] + i
                if x < 0 or x >= board_width or y >= board_height or (y >= 0 and board[y][x] != 0):
                    return True
    return False

# テトリミノのロック
def lock_tetromino(tetromino):
    shape = tetromino['shape']
    color = tetromino['color']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                board[tetromino['y'] + i][tetromino['x'] + j] = color

# テトリミノの移動
def move_tetromino(tetromino, dx, dy):
    tetromino['x'] += dx
    tetromino['y'] += dy
    if check_collision(tetromino):
        tetromino['x'] -= dx
        tetromino['y'] -= dy
        return False
    return True

# 行の消去
def clear_lines():
    global score
    lines_to_clear = []
    for i, row in enumerate(board):
        if all(cell != 0 for cell in row):
            lines_to_clear.append(i)
    
    # スコアの加算
    score += 10 * len(lines_to_clear)
    
    # 行を消去
    for i in lines_to_clear:
        del board[i]
        board.insert(0, [0] * board_width)

# ゴーストテトリミノの描画
def draw_ghost(tetromino):
    ghost_tetromino = tetromino.copy()
    while move_tetromino(ghost_tetromino, 0, 1):
        pass
    shape = ghost_tetromino['shape']
    color = (255, 255, 255)  # ゴーストの色（白）
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color,
                                 ((ghost_tetromino['x'] + j) * block_size,
                                  (ghost_tetromino['y'] + i) * block_size,
                                  block_size, block_size))

# ゲームオーバーの判定
def check_game_over():
    for cell in board[0]:
        if cell != 0:
            return True
    return False

# ゲームのリスタート
def restart_game():
    global board, score, current_tetromino, fall_speed
    board = [[0] * board_width for _ in range(board_height)]
    score = 0
    current_tetromino = create_tetromino()
    return 500  # 初期の落下速度を返す

# スピードを更新する関数
def update_speed():
    global fall_speed
    fall_speed = max(100, 500 - (score // 50) * 50)  # スコアに応じてスピードを増加

# メインループ
running = True
paused = False
clock = pygame.time.Clock()
current_tetromino = create_tetromino()
fall_time = 0
fall_speed = restart_game()  # ゲーム開始時に速度を初期化

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_tetromino(current_tetromino, -1, 0)
            elif event.key == pygame.K_RIGHT:
                move_tetromino(current_tetromino, 1, 0)
            elif event.key == pygame.K_UP:
                rotate_tetromino(current_tetromino)
            elif event.key == pygame.K_p:  # ポーズ
                paused = not paused
            elif event.key == pygame.K_r and check_game_over():  # リスタート
                fall_speed = restart_game()

    keys = pygame.key.get_pressed()  # 現在押されているキーを取得
    if keys[pygame.K_DOWN]:  # 下のボタンが押されている間
        move_tetromino(current_tetromino, 0, 1)  # 常に下に移動

    if not paused:
        # 自動でテトリミノを下に移動
        current_time = pygame.time.get_ticks()
        if current_time - fall_time > fall_speed:
            if not move_tetromino(current_tetromino, 0, 1):
                lock_tetromino(current_tetromino)
                clear_lines()
                update_speed()  # スピードを更新
                current_tetromino = create_tetromino()
                if check_game_over():  # ゲームオーバーの判定
                    paused = True  # ゲームオーバー時にポーズする
            fall_time = current_time

    # ボードの描画
    for y in range(board_height):
        for x in range(board_width):
            if board[y][x] != 0:
                pygame.draw.rect(screen, colors[board[y][x]],
                                 (x * block_size, y * block_size, block_size, block_size))

    # テトリミノの描画
    shape = current_tetromino['shape']
    color = current_tetromino['color']
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[color],
                                 ((current_tetromino['x'] + j) * block_size,
                                  (current_tetromino['y'] + i) * block_size,
                                  block_size, block_size))

    # ゴーストテトリミノの描画
    draw_ghost(current_tetromino)

    # スコアの表示
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # ゲームオーバー時の表示
    if check_game_over():
        game_over_text1 = font.render('Game Over!', True, (255, 0, 0))
        game_over_text2 = font.render('Press R to Restart', True, (255, 0, 0))
        screen.blit(game_over_text1, (screen_width // 8, screen_height // 2))
        screen.blit(game_over_text2, (screen_width // 8, screen_height // 2 + 40))  # 40ピクセル下に配置

    pygame.display.update()
    clock.tick(30)  # フレームレート設定

pygame.quit()
