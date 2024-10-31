import pygame
import random

# 初期化
pygame.init()

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger風ゲーム")

# 色の定義
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# プレイヤー設定
player_size = 40
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_size
player_speed = 10
player_lives = 3  # ライフの初期設定

# 障害物設定
obstacle_width = 60
obstacle_height = 30
obstacle_speed = 5
obstacle_list = []

# アイテム設定
item_size = 30
item_list = []
boost_active = False
boost_duration = 3000  # ブーストの持続時間（ミリ秒）
boost_end_time = 0
invincible_active = False
invincible_duration = 3000  # 無敵の持続時間（ミリ秒）
invincible_end_time = 0

# 水エリア設定
log_width = 100
log_height = 20
log_speed = 3
log_list = []

# スコアとレベル
score = 0
level = 1

# タイマー設定
time_limit = 30000  # 30秒
start_time = pygame.time.get_ticks()

# ゲームループ用のフラグ
running = True
goal_reached = False

# フレームレート設定
clock = pygame.time.Clock()
FPS = 30

# フォント設定
font = pygame.font.Font(None, 36)

# サウンド設定
pygame.mixer.init()
hit_sound = pygame.mixer.Sound('hit.wav')  # 衝突音
goal_sound = pygame.mixer.Sound('goal.wav')  # ゴール音
item_sound = pygame.mixer.Sound('item.wav')  # アイテム取得音
bgm = pygame.mixer.music.load('bgm.mp3')  # BGM
pygame.mixer.music.play(-1)

def create_obstacle():
    """障害物を画面上部に作成し、ランダムな位置に配置する"""
    x_pos = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y_pos = random.choice([-obstacle_height, SCREEN_HEIGHT])
    direction = random.choice([-1, 1])
    obstacle_list.append([x_pos, y_pos, direction * obstacle_speed])

def create_log():
    """水エリアにログを生成する"""
    x_pos = random.randint(0, SCREEN_WIDTH - log_width)
    y_pos = random.randint(150, 300)
    direction = random.choice([-1, 1])
    log_list.append([x_pos, y_pos, direction * log_speed])

def create_item():
    """アイテムをランダムに生成"""
    x_pos = random.randint(0, SCREEN_WIDTH - item_size)
    y_pos = random.randint(0, SCREEN_HEIGHT - item_size)
    item_list.append([x_pos, y_pos])

def move_obstacles():
    """障害物を移動させる"""
    for obstacle in obstacle_list:
        obstacle[1] += obstacle[2]
    obstacle_list[:] = [ob for ob in obstacle_list if 0 <= ob[1] < SCREEN_HEIGHT]

def move_logs():
    """ログを移動させる"""
    for log in log_list:
        log[0] += log[2]
        if log[0] < -log_width:
            log[0] = SCREEN_WIDTH
        elif log[0] > SCREEN_WIDTH:
            log[0] = -log_width

def check_collision():
    """プレイヤーと障害物の衝突判定"""
    if invincible_active:
        return False
    for obstacle in obstacle_list:
        if (player_x < obstacle[0] + obstacle_width and
            player_x + player_size > obstacle[0] and
            player_y < obstacle[1] + obstacle_height and
            player_y + player_size > obstacle[1]):
            return True
    return False

def check_item_collision():
    """プレイヤーとアイテムの衝突判定"""
    global boost_active, invincible_active, boost_end_time, invincible_end_time
    for item in item_list:
        if (player_x < item[0] + item_size and
            player_x + player_size > item[0] and
            player_y < item[1] + item_size and
            player_y + player_size > item[1]):
            item_list.remove(item)
            item_sound.play()
            # 効果をランダムに決定
            if random.choice([True, False]):
                boost_active = True
                boost_end_time = pygame.time.get_ticks() + boost_duration
            else:
                invincible_active = True
                invincible_end_time = pygame.time.get_ticks() + invincible_duration

def update_game_state():
    """ゲームの状態を更新"""
    global player_speed, boost_active, invincible_active, score, level, player_lives, goal_reached

    # ブーストの効果
    if boost_active and pygame.time.get_ticks() > boost_end_time:
        boost_active = False

    # 無敵の効果
    if invincible_active and pygame.time.get_ticks() > invincible_end_time:
        invincible_active = False

    # ゴール判定
    if player_y <= 0:
        goal_sound.play()
        goal_reached = True
        score += 100 * level
        level += 1

    # 衝突判定
    if check_collision():
        player_lives -= 1
        hit_sound.play()
        if player_lives <= 0:
            running = False

def draw_game():
    """ゲームの描画"""
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, 0, SCREEN_WIDTH, player_size))  # ゴールライン
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))  # プレイヤー
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))
    for log in log_list:
        pygame.draw.rect(screen, BLUE, (log[0], log[1], log_width, log_height))
    for item in item_list:
        pygame.draw.circle(screen, YELLOW, (item[0] + item_size // 2, item[1] + item_size // 2), item_size // 2)
    # スコア、レベル、ライフの表示
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(lives_text, (10, 90))
    pygame.display.flip()

# ゲームループ
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and goal_reached:
                player_y = SCREEN_HEIGHT - player_size
                goal_reached = False
                create_obstacle()
                create_log()

    # プレイヤーの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed if not boost_active else player_speed * 2
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
        player_x += player_speed if not boost_active else player_speed * 2
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed if not boost_active else player_speed * 2
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_size:
        player_y += player_speed if not boost_active else player_speed * 2

    # ゲームの状態を更新
    update_game_state()
    move_obstacles()
    move_logs()
    check_item_collision()

    # ゲームの描画
    draw_game()

    # タイマーのチェック
    if pygame.time.get_ticks() - start_time > time_limit:
        running = False

    # フレームレートの設定
    clock.tick(FPS)

# ゲーム終了
pygame.quit()
