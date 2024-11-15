import pygame,math
from pygame.locals import *
import sys
import numpy
from numpy import array

def main():
    pygame.init()
    screen = pygame.display.set_mode((680, 450))
    pygame.display.set_caption("壁ズリ　テスト")
    font = pygame.font.Font(None, 30)
    (x,y)=(100.0,100.0)
    (a1,a2,b1,b2)=(100,200,300,100)
    while (1):
        screen.fill((255,255,255))   # 背景を白で塗りつぶし
        #移動用のベクトルを作成
        move = array([0.0,0.0])
        #押されたキーによって移動用のベクトルに移動量を代入
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            move[0]= -0.1
        if pressed_key[K_RIGHT]:
            move[0]= 0.1
        if pressed_key[K_UP]:
            move[1]= -0.1
        if pressed_key[K_DOWN]:
            move[1]= 0.1
        #押されたキーに応じて移動量のベクトルに入れる
        #移動量は壁ズリの処理が必要ないときに実行させる
        #壁の描写（始点をa、終点をbとする（緑色の線）
        pygame.draw.line(screen, (0,255,0), (a1,a2), (b1,b2), 5)   # 直線の描画

        #プレイヤーの描写
        pygame.draw.ellipse(screen,(255,0,0),(x-15,y-15,30,30))

        #////////////////ここから下は壁とプレイヤーに垂線を引くための計算////////
        ab_v = array([b1-a1,b2-a2]) #壁のa点とb点の間のベクトル
        ap_v = array([x-a1,y-a2]) #壁の点1と自分の座標の間のベクトル
        #壁のベクトルabの単位ベクトルにするための一時的計算
        temp = math.sqrt( pow(ab_v[0],2) + pow(ab_v[1],2) )
        #壁のベクトルの単位ベクトルを計算
        n_v = array([ab_v[0]/temp,ab_v[1]/temp])
        #壁のa点から垂線までの距離を計算するために壁の単位ベクトルと壁の点1と自分の座標の間のベクトルの内積を計算する
        temp = numpy.inner(n_v,ap_v)
        #壁の始点aに壁の単位ベクトルに垂線までの距離をかけたもので垂線の座標をだす
        p_v = array([a1+n_v[0]*temp,a2+n_v[1]*temp])
        #ただし垂線の座標が壁のxの範囲を超えているときは補正する
        if(p_v[0] <= a1):
            p_v[0] = a1
        if(b1 <= p_v[0]):
            p_v[0] = b1
        #ただし垂線の座標が壁のyの範囲を超えているときは補正する
        if(a2<=p_v[1]):
            p_v[1]=a2
        if(p_v[1]<=b2):
            p_v[1]=b2
        #壁の始点aに壁の単位ベクトルに垂線までの距離をかけたもので垂線の座標をだす
        pygame.draw.line(screen, (0,0,255), (x,y), (p_v[0],p_v[1]), 5)   # 直線の描画
        #////////////////ここまで/////////////////////

        #////////////////壁ズリの計算////////
        #垂線の座標とプレイヤーの座標をもとにベクトルを作る（青色の線）
        housen = array([x-p_v[0] , y-p_v[1]])
        #現在の座標に移動予定の座標を足したものがプレイヤーに接触するか計算するために距離を出す
        kyori = math.sqrt( pow(housen[0]+move[0],2) + pow(housen[1]+move[1],2) )

        #もし接触していたら
        if  kyori <= 15:
            #法線ベクトルの単位ベクトルにするための一時的計算
            temp_a = math.sqrt( pow(housen[0],2) + pow(housen[1],2) )
            #法線ベクトルの単位ベクトルを計算
            n_v = array([housen[0]/temp_a,housen[1]/temp_a])
            #壁ズリのために修正しないといけない移動量を計算するためにベクトルの内積を計算する
            temp_a = -numpy.inner(move,n_v)
            x += move[0]+temp_a*n_v[0]
            y += move[1]+temp_a*n_v[1]
        #接触していなかったら保留していた移動を許可する
        else:
            x += move[0]
            y += move[1]
        pygame.display.update()     # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()

if __name__ == "__main__":
    main()