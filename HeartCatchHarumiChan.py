# -*- coding: utf-8 -*-

import time
import tkinter
import random
import os
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageChops

############################################################################### 
# 初期処理
############################################################################### 

# 仮想VRAMのサイズ
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 25

# ゲームの状態
GAMESTATUS_TITLE = 0
GAMESTATUS_GAME = 1
GAMESTATUS_MISS = 2
GAMESTATUS_CLEAR = 3
GAMESTATUS_OVER = 4

# キー判定用
KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_SPACE = "space"
KEY_S = "s"

# PC8001のカラーコードとRGB値の対応辞書
# 0 : 黒        RGB( 0x00, 0x00, 0x00)
# 1 : 青        RGB( 0x00, 0x00, 0xFF)
# 2 : 赤        RGB( 0xFF, 0x00, 0x00)
# 3 : マゼンタ  RGB( 0xFF, 0x00, 0xFF)
# 4 : 緑        RGB( 0x00, 0xFF, 0x00)
# 5 : シアン    RGB( 0x00, 0xFF, 0xFF)
# 6 : 黄色      RGB( 0xFF, 0xFF, 0x00)
# 7 : 白        RGB( 0xFF, 0xFF, 0xFF)
COLOR = {
    "BLACK"  : (0x00, 0x00, 0x00),
    "BLUE"   : (0x00, 0x00, 0xFF),
    "RED"    : (0xFF, 0x00, 0x00),
    "MAGENTA": (0xFF, 0x00, 0xFF),
    "GREEN"  : (0x00, 0xFF, 0x00),
    "CYAN"   : (0x00, 0xFF, 0xFF),
    "YELLOW" : (0xFF, 0xFF, 0x00),
    "WHITE"  : (0xFF, 0xFF, 0xFF),
}

# PC8001のカラーコード
COLOR_0 = "BLACK"
COLOR_1 = "BLUE"
COLOR_2 = "RED"
COLOR_3 = "MAGENTA"
COLOR_4 = "GREEN"
COLOR_5 = "CYAN"
COLOR_6 = "YELLOW"
COLOR_7 = "WHITE"

# スクリプトのパス
basePath = os.path.abspath(os.path.dirname(__file__))

# PhotoImageの保存用変数
photoImage = ""

# ゲームの状態管理用
gameStatus = GAMESTATUS_TITLE

# ゲームの経過時間管理用
gameTime = 0

# キーイベント用
key = ""
keyOff = True

# 画面フラッシュ制御用
flash1_flg = False
flash2_flg = False

# タイトルアニメーション用
title_x = 0
harumi_y = 0

# プテラノドン
ptera_x = 25
ptera_y = 16
ptera_old_x = 25
ptera_old_y = 16
ptera_pattern = 1

# you
you_x = 10
you_v = 1

# ボール
ball_status = 0
ball_x = 0
ball_y = 0
ball_old_x = 0
ball_old_y = 0

# スコア
score = 100
hiscore = 100

# チャンス
chance = 3

# プテラノドンを倒した数
destroy = 0

# ハートの座標
heart_x = 2
heart_y = 19
heart_old_x = 0
heart_old_y = 0


############################################################################### 
# メイン処理
############################################################################### 
def main():
    global gameTime, key, keyOff

    # 画面描画
    draw()


    # 処理
    if gameStatus == GAMESTATUS_TITLE:
        # タイトル処理
        title()

    elif gameStatus == GAMESTATUS_GAME:
        # ゲームメイン処理
        game()		

    elif gameStatus == GAMESTATUS_MISS:
        # ミス処理
        miss()		

    elif gameStatus == GAMESTATUS_OVER:
        # ゲームオーバー処理
        gameover()		

    elif gameStatus == GAMESTATUS_CLEAR:
        # ゲームクリア処理
        gameclear()


    # 時間進行
    gameTime = gameTime + 1

    # キーリピート対策
    if keyOff == True:
        key = ""
        keyOff = False

    root.after(50, main)


############################################################################### 
# キーイベント：キー押す
############################################################################### 
def pressKey(e):
    global key, keyOff

    key = e.keysym
    keyOff = False


############################################################################### 
# キーイベント：キー離す
############################################################################### 
def releaseKey(e):
    global keyOff

    keyOff = True


############################################################################### 
# ゲーム状態変更
############################################################################### 
def changeGameStatus(status):
    global gameStatus, gameTime

    gameStatus = status
    gameTime = 0


############################################################################### 
# タイトル処理
############################################################################### 
def title():
    global key, title_x, harumi_y, flash1_flg

    if gameTime == 1:
        title_x = -1
        harumi_y = -1

    if gameTime < 9:
        if gameTime % 2 == 0:
            flash1_flg = True

    if gameTime == 10:
        title_x = 28

    if gameTime > 10 and gameTime < 40:
        title_x = (title_x - 1) if title_x > 0 else 0

    if gameTime == 40:
        harumi_y = 3

    if gameTime > 40 and gameTime < 55:
        harumi_y = (harumi_y + 1) if harumi_y < 16 else 15

    if gameTime > 55 and key == KEY_S:
        # ゲーム初期化
        initializeGame()
        retryGame()
        changeGameStatus(GAMESTATUS_GAME)

    key = ""


############################################################################### 
# ゲーム初期化
############################################################################### 
def initializeGame():
    global score, chance, destroy, heart_x, heart_y, heart_old_x, heart_old_y

    # スコア
    score = 100

    # チャンス
    chance = 3

    # プテラノドンを倒した数
    destroy = 0

    # ハートの座標
    heart_x = 2
    heart_y = 19
    heart_old_x = 0
    heart_old_y = 0


############################################################################### 
# ゲーム再開
############################################################################### 
def retryGame():
    global ptera_x, ptera_y, ptera_old_x, ptera_old_y, ptera_pattern, you_x, you_v, ball_status, ball_x, ball_y, ball_old_x, ball_old_y

    # プテラノドン
    ptera_x = 25
    ptera_y = 16
    ptera_old_x = 25
    ptera_old_y = 16
    ptera_pattern = 1

    # you
    you_x = 11
    you_v = 1

    # ボール
    ball_status = 0
    ball_x = 0
    ball_y = 0
    ball_old_x = 0
    ball_old_y = 0


############################################################################### 
# ゲーム処理
############################################################################### 
def game():
    global key, score, destroy, you_x, you_v, ball_status, ball_old_x, ball_old_y, ball_x, ball_y, ptera_pattern, ptera_x, ptera_y, ptera_old_x, ptera_old_y

    # ボールの処理
    if ball_status > 0:
        if ball_status == 4:
            # ボール消す
            ball_status = 0
            # 減点
            score = score - 10

        elif ball_status == 5:
            # プテラノドン落ちる
            ptera_old_x = ptera_x
            ptera_old_y = ptera_y
            ptera_y = ptera_y + 1
            if ptera_y > 22:
                ball_status = 0
                destroy = destroy + 1
                if destroy > 15:
#                if destroy > 3:
                    changeGameStatus(GAMESTATUS_CLEAR)
                else:
                    ptera_old_x = ptera_x
                    ptera_old_y = 22
                    ptera_x = random.randint(14, 34)
                    ptera_y = 16
 
        elif ball_status < 3:
            ball_status = ball_status + 1

        else:
            ball_old_x = ball_x
            ball_old_y = ball_y
            ball_x = ball_x + you_v
            ball_y = ball_y - 1

            # ボール画面外？
            if ball_x < 12 or ball_x > 37 or ball_y < 4:
                ball_status = 4

            # ボールヒット？
            if ball_x == ptera_x + 2 and ball_y == ptera_y:
                score = score + 200 - ptera_y * 10
                ball_status = 5

    else:
        # ミス判定
        if ptera_y == 3:
            changeGameStatus(GAMESTATUS_MISS)

        # ゲームオーバー判定
        if score == 0:
            changeGameStatus(GAMESTATUS_OVER)

        # ボール投げる？
        if key == KEY_SPACE and ball_status == 0:
            ball_status = 1
            ball_x = you_x + (5 if you_v == 1 else 1)
            ball_y = 18
            ball_old_x = ball_x
            ball_old_y = ball_y

        else:
            # YOU操作
            if key == KEY_LEFT and you_x > 10:
                you_x = you_x - 1
                you_v = -1

            if key == KEY_RIGHT and you_x < 35:
                you_x = you_x + 1
                you_v = 1

            # プテラノドンを動かす
            if gameTime % 2 == 0:
                ptera_old_x = ptera_x
                ptera_old_y = ptera_y
                ptera_pattern = 1 - ptera_pattern
                ptera_y = ptera_y + ptera_pattern * -(random.randint(0, 5) < 4)
                if ptera_x > 13 and ptera_x < 33:
                    ptera_x = ptera_x + (random.randint(0, 2) - 1)

    key = ""


############################################################################### 
# ミス処理
############################################################################### 
def miss():
    global chance

    if gameTime > 30:
        chance = chance - 1
        if chance == 0:
            changeGameStatus(GAMESTATUS_OVER)
        else:
            retryGame()
            changeGameStatus(GAMESTATUS_GAME)


############################################################################### 
# ゲームオーバー処理
############################################################################### 
def gameover():
    global hiscore

    if gameTime == 1:
        if score > hiscore:
            hiscore = score
    
    if gameTime > 40 and key == KEY_S:
        changeGameStatus(GAMESTATUS_TITLE)


############################################################################### 
# ゲームクリア処理
############################################################################### 
def gameclear():
    global heart_x, heart_y, heart_old_x, heart_old_y

    if gameTime % 2 == 0:
        heart_old_x = heart_x
        heart_old_y = heart_y

        heart_x = heart_x + 1
        if heart_x < 18:
            heart_y = heart_y + random.randint(0, 2) - 1 - (heart_y > 19)

    if gameTime == 40:
        changeGameStatus(GAMESTATUS_OVER)


############################################################################### 
# 画面描画
############################################################################### 
def draw():
    global photoImage, flash1_flg, flash2_flg

    # canvasのイメージ削除
    canvas.delete("SCREEN")

    if gameStatus == GAMESTATUS_TITLE:
        # タイトル
        drawTitle()

    elif gameStatus == GAMESTATUS_GAME:
        # ゲーム画面
        drawGame()

    elif gameStatus == GAMESTATUS_MISS:
        # ミス画面
        drawMiss()

    elif gameStatus == GAMESTATUS_OVER:
        # ゲームオーバー画面
        drawGameOver()

    elif gameStatus == GAMESTATUS_CLEAR:
        # ゲームクリア画面
        drawGameClear()


    # 画面表示用イメージ生成
    img_screen = img_text.copy()

    # フラッシュ１処理
    # うまくいってない
    if flash1_flg == True:
        flash1_flg = False
        plane = img_screen.split()
        _r = plane[0].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        _g = plane[1].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        _b = plane[2].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        img_mask = ImageChops.logical_and(_r, _g)
        img_mask = ImageChops.logical_and(img_mask, _b)
        img_screen.paste(Image.new("RGB", img_text.size, (200, 200, 200)), mask = img_mask)

    # フラッシュ２処理
    if flash2_flg == True:
        flash2_flg = False
        img_screen = Image.new("RGB", (SCREEN_WIDTH * 8, SCREEN_HEIGHT * 8), (0xFA, 0xFA, 0xFA))

    # 画面イメージを拡大
    img_screen = img_screen.resize((img_screen.width * 2, img_screen.height * 2), Image.NEAREST)

    # オフスクリーンでPhotoImage生成
    photoImage = ImageTk.PhotoImage(img_screen)
    canvas.create_image((img_screen.width / 2, img_screen.height / 2), image = photoImage, tag = "SCREEN")


############################################################################### 
# タイトル画面描画
############################################################################### 
def drawTitle():
    global flash1_flg

    # 画面イメージ作成
    if gameTime == 1:
        cls()
        writeText(0, 0, (0x97, 0x20, 0x88, 0x20, 0x20, 0x20, 0x97, 0x20, 0x20, 0x20, 0x20, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x80, 0x80, 0xEE), COLOR_2)
        writeText(0, 1, (0x97, 0x20, 0x88, 0x95, 0x95, 0x95, 0x97, 0xEF, 0x20, 0x20, 0xE9, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x95, 0x8F, 0x95), COLOR_2)
        writeText(0, 2, (0xEE, 0x20, 0xEF, 0x20, 0x20, 0x20, 0x97, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x96, 0x20, 0x20, 0xD4, 0x20, 0xC2, 0x20, 0x95, 0x9B, 0x20), COLOR_2)

    # フラッシュ
    if gameTime < 9:
        if gameTime % 2 == 0:
            flash1_flg = True

    # タイトル文字移動
    if gameTime > 10 and gameTime < 40:
        writeText(title_x, 3, (0x20, 0x20, 0xEF, 0xED, 0x80, 0x20), COLOR_3)
        writeText(title_x, 4, (0x20, 0x20, 0x20, 0x87, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x97, 0x20, 0x88, 0x20, 0x97, 0x97, 0x20, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x80, 0x80, 0xEE, 0x20, 0x20, 0x20, 0x95, 0x20, 0x97, 0x20), COLOR_3)
        writeText(title_x, 5, (0x9C, 0xE0, 0xE0, 0xEF, 0xEF, 0xE0, 0xE0, 0x9D, 0xE0, 0x20, 0x97, 0x20, 0x88, 0x20, 0x97, 0x97, 0x20, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x97, 0x20), COLOR_3)
        writeText(title_x, 6, (0x9E, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0x9F, 0xE0, 0x20, 0xEE, 0x20, 0xEF, 0x20, 0xEE, 0x97, 0xEE, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x95, 0x9B, 0x20, 0x20, 0xD4, 0x20, 0x80, 0x80, 0xEE, 0x20), COLOR_3)

    # ハルミチャン
    if gameTime > 40 and gameTime < 55:
        img_text.paste(img_harumi00, (gPos(2), gPos(harumi_y)))

    # タイトル
    if gameTime == 55:
        # UFO消去
        writeText( 0,  5, [0x20] * 9)
        writeText( 0,  6, [0x20] * 9)
        # プテラノドン
        writeText(27, 15, ptera[1][0], COLOR_1)
        writeText(29, 16, ptera[1][1], COLOR_1)
        # "プログラミング レッスン"
        writeText(10,  9, (0x3D, 0x20, 0xCC, 0xDF, 0xDB, 0xB8, 0xDE, 0xD7, 0xD0, 0xDD, 0xB8, 0xDE, 0x20, 0xE9, 0x20, 0xDA, 0xAF, 0xBD, 0xDD, 0x20, 0x3D), COLOR_6) 
        # "ハルミチャン"
        writeText( 1, 21, (0xCA, 0xD9, 0xD0, 0xC1, 0xAC, 0xDD), COLOR_7)
        # "プテラノドン"
        writeText(24, 21, (0xCC, 0xDF, 0xC3, 0xD7, 0xC9, 0xC4, 0xDE, 0xDD), COLOR_7)
        # "YOU!"
        img_text.paste(img_you[0], (gPos(14), gPos(14)))
        writeText(18, 18, ("< YOU!"), COLOR_7)
        # その他の表示
        writeText(13, 21, (0x31, 0x20, 0x3C, 0x2D, 0x3E, 0x20, 0x33), COLOR_7)
        writeText(10, 22, (0x42, 0x41, 0x4C, 0x4C, 0x20, 0x3D, 0x20, 0x53, 0x50, 0x41, 0x43, 0x45), COLOR_7)
        writeText(13, 24, (0x50, 0x55, 0x53, 0x48, 0x20, 0x5B, 0x53, 0x5D, 0x20, 0x21), COLOR_7)


############################################################################### 
# ゲーム画面描画
############################################################################### 
def drawGame():

    # 画面イメージ作成
    if gameTime == 1:
        cls()
        writeText(0, 0, (0x5B, 0x3A, 0x53, 0x43, 0x4F, 0x52, 0x45, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x5D, 0x20, 0xE9, 0x20, 0xCA, 0xB0, 0xC4, 0x20, 0xB7, 0xAC, 0xAF, 0xC1, 0x20, 0x5B, 0x3A, 0x42, 0x49, 0x52, 0x44, 0x53, 0x20, 0x20, 0x20, 0x20, 0x5D), COLOR_7)
        writeText(0, 1, (0xE2, 0xE2, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE2, 0xE0, 0xE0, 0xE0, 0xE0, 0x20, 0x20, 0xCA, 0xD9, 0xD0, 0x20, 0xC1, 0xAC, 0xDD, 0x20, 0xE9, 0x20, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0), COLOR_7)
        writeText(0, 2, (0xE2, 0xE2, 0x20, 0x43, 0x48, 0x41, 0x4E, 0x43, 0x45, 0x20, 0x20, 0x20, 0xE2, 0x20, 0x20, 0x20, 0x20, 0x20, 0x50, 0x52, 0x4F, 0x47, 0x52, 0x41, 0x4D, 0x4D, 0x49, 0x4E, 0x47, 0x20, 0x4C, 0x45, 0x53, 0x53, 0x4F, 0x4E, 0x20, 0x20), COLOR_7)
        writeText(0, 3, (0xE2, 0xE2, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE2, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0), COLOR_7)
        for i in range(6):
            writeText(0, 4 + i, (0x96, 0x96), COLOR_7)

        writeText(0, 10, (0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5), COLOR_2)
        writeText(0, 11, (0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5), COLOR_2)
        writeText(0, 12, (0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5), COLOR_2)
        writeText(0, 13, (0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5), COLOR_2)
        writeText(0, 14, (0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5), COLOR_2)
        writeText(0, 15, (0x20, 0xEE, 0x96, 0xEF, 0x20, 0x20, 0x20, 0x20, 0x20, 0x87), COLOR_6)
        writeText(0, 16, (0xEC, 0xEC, 0xEC, 0xEC, 0xEC, 0x20, 0x20, 0x20, 0x20, 0x87), COLOR_6)

        writeText(0, 20, (0x20, 0x20, 0x20, 0x20, 0x9C, 0x95, 0x9D), COLOR_7)
        writeText(0, 21, (0x9D, 0x20, 0x20, 0x9C, 0x90, 0x9D, 0xE3), COLOR_7)
        writeText(0, 22, (0x96, 0x20, 0x20, 0x8F, 0x90, 0x90, 0x8F, 0x9D), COLOR_7)
        writeText(0, 23, (0x9E, 0x91, 0x20, 0xE1, 0xE0, 0xE0, 0xE3, 0x9E, 0x65), COLOR_7)

        writeText(5, 16, (0x9C, 0x95, 0x9D), COLOR_5)
        writeText(5, 17, (0x96, 0x9A, 0x96), COLOR_5)
        writeText(5, 18, (0x9E, 0x95, 0x9F), COLOR_5)

        writeText(1, 20, (0xED), COLOR_3)
        writeText(1, 21, (0x87, 0xEF), COLOR_3)
        writeText(1, 22, (0x87, 0xE5), COLOR_3)
        writeText(2, 23, (0xEF), COLOR_3)

        for i in range(7):
            writeText(9, 17 + i, (0x87), COLOR_6)

        for i in range(39):
            writeText(i , 24, (0x85), COLOR_1)            

        # チャンス
        writeText(10, 2, (str(chance)), COLOR_7)

    # スコア
    writeText( 8, 0, ("{: 5}".format(score)), COLOR_7)

    # プテラノドン残り
    writeText(34, 0, ("{: 3}".format(destroy)), COLOR_7)

    # YOU描画
    if ball_status == 1:
        img_text.paste(img_you[5 if you_v == 1 else 3], (gPos(you_x + 1), gPos(18)))
    elif ball_status > 1:
        img_text.paste(img_you[6 if you_v == 1 else 4], (gPos(you_x + 1), gPos(18)))
    else:
        img_text.paste(img_you[2 if you_v == 1 else 1], (gPos(you_x + 1), gPos(18)))

    # ボール描画
    if ball_status > 2:
        writeText(ball_old_x, ball_old_y, (0x20), COLOR_6)
        if ball_status == 3:
            writeText(ball_x, ball_y, (0xEC), COLOR_6)
        if ball_status == 5:
            # プテラノドン消去
            writeText(ptera_old_x    , ptera_old_y    , ptera[0][0], COLOR_1)
            writeText(ptera_old_x + 2, ptera_old_y + 1, ptera[0][1], COLOR_1)
            if ptera_y < 23:
                # プテラノドン描画
                writeText(ptera_x    , ptera_y    , ptera[1][0], COLOR_1)
                writeText(ptera_x + 2, ptera_y + 1, ptera[1][1], COLOR_1)

    else:
        # プテラノドン消去
        writeText(ptera_old_x    , ptera_old_y    , ptera[0][0], COLOR_1)
        writeText(ptera_old_x + 2, ptera_old_y + 1, ptera[0][1], COLOR_1)
        # プテラノドン描画
        writeText(ptera_x    , ptera_y    , ptera[ptera_pattern + 1][0], COLOR_1)
        writeText(ptera_x + 2, ptera_y + 1, ptera[ptera_pattern + 1][1], COLOR_1)

        # ハルミチャンのタイピング
        if ptera_pattern == 0:
            writeText( 2, 21, (0x94), COLOR_3)
        else:
            writeText( 2, 21, (0xEF), COLOR_3)


############################################################################### 
# ミス画面描画
############################################################################### 
def drawMiss():
    global flash2_flg

    if gameTime < 40 and gameTime % 2 == 0:
        flash2_flg = True

    else:
        writeText( 0, 18, (0xB4, 0xB0, 0xDD, 0x21), COLOR_6)
        writeText( 0, 19, (0x2E, 0x21, 0x2E), COLOR_6)
        writeText( 0, 20, (0xEF, 0x78, 0xEE), COLOR_3)
        writeText( 2, 21, (0x20), COLOR_3)
       

############################################################################### 
# ゲームオーバー画面描画
############################################################################### 
def drawGameOver():

    if gameTime < 40:
        writeText( 39 - gameTime, 5, (0x20, 0x20, 0x20, 0x20, 0x20, 0x98, 0x20, 0x98, 0x95, 0x99, 0x98, 0x95, 0x99, 0x98, 0x91, 0x99, 0x91, 0x95, 0x99, 0x20, 0x98, 0x95, 0x99, 0x91, 0x20, 0x91, 0x91, 0x95, 0x99, 0x91, 0x95, 0x99, 0x20, 0x99, 0x20, 0x20, 0x20, 0x20, 0x20), COLOR_4)
        writeText(-39 + gameTime, 6, (0x20, 0x20, 0x20, 0x20, 0x20, 0x96, 0x20, 0x96, 0x20, 0x99, 0x93, 0x95, 0x92, 0x96, 0x96, 0x96, 0x93, 0x92, 0x20, 0x20, 0x96, 0x20, 0x96, 0x96, 0x20, 0x96, 0x93, 0x92, 0x20, 0x93, 0x91, 0x9B, 0x20, 0x96, 0x20, 0x20, 0x20, 0x20, 0x20), COLOR_4)
        writeText( 39 - gameTime, 7, (0x20, 0x20, 0x20, 0x20, 0x20, 0x9A, 0x20, 0x9A, 0x95, 0x9B, 0x90, 0x20, 0x90, 0x90, 0x20, 0x90, 0x90, 0x95, 0x9B, 0x20, 0x9A, 0x95, 0x9B, 0x9A, 0x95, 0x9B, 0x90, 0x95, 0x9B, 0x90, 0x9A, 0x9B, 0x20, 0x9B, 0x20, 0x20, 0x20, 0x20, 0x20), COLOR_4)

    if gameTime == 40:
        writeText(12, 17, ("HI-SCORE : " + str(hiscore) + " Pts."), COLOR_6)
        writeText(15, 20, ("PUSH [S] !"), COLOR_7)
       

############################################################################### 
# ゲームクリア画面描画
############################################################################### 
def drawGameClear():

    if gameTime == 1:
        writeText(ptera_old_x    , ptera_old_y    , ptera[0][0], COLOR_1)
        writeText(ptera_old_x + 2, ptera_old_y + 1, ptera[0][1], COLOR_1)

    if gameTime < 40:
        if heart_old_x > 0 and heart_old_y > 0:
            writeText(heart_old_x, heart_old_y, (0x20), COLOR_2)
        writeText(heart_x    , heart_y    , (0xE9), COLOR_2)

    else:
        writeText(heart_x, heart_y, (0x20), COLOR_2)
        writeText(17, 10, (0x20, 0xE9, 0xE9, 0x20, 0xE9, 0xE9, 0x20), COLOR_2)
        writeText(17, 11, (0xE9, 0x20, 0x20, 0xE9, 0x20, 0x20, 0xE9), COLOR_2)
        writeText(17, 12, (0xE9, 0x20, 0x20, 0x20, 0x20, 0x20, 0xE9), COLOR_2)
        writeText(17, 13, (0x20, 0xE9, 0x20, 0x20, 0x20, 0xE9, 0x20), COLOR_2)
        writeText(17, 14, (0x20, 0x20, 0xE9, 0x20, 0xE9, 0x20, 0x20), COLOR_2)
        writeText(17, 15, (0x20, 0x20, 0x20, 0xE9, 0x20, 0x20, 0x20), COLOR_2)


############################################################################### 
# テキスト描画
# 引数		x, y テキスト座標系の座標
#			s 表示する文字データの配列（文字の場合は、文字コードに対応した文字を表示する）
#           c 文字の表示色（省略時は白）
############################################################################### 
def writeText(x, y, s, c=COLOR_7):
    global img_text

    # 指定色で塗りつぶした矩形を作成
    if type(s) is int:
        s = [s]

    imgBack = Image.new("RGBA", (gPos(len(s)), 8), COLOR[c])
    
    # 文字を描画
    for i in range(len(s)):
        if isinstance(s, str):
            o = ord(s[i]) - 32
        else:
            o = s[i] - 32

        if o >= 0 and o <= len(img_font):
            imgBack.paste(img_font[o], (gPos(i), gPos(0)), img_font_mask[o])

    # 文字のパターンでマスクした画像を貼り付け
    img_text.paste(imgBack, (gPos(x), gPos(y)), imgBack)


############################################################################### 
# テキスト画面クリア
############################################################################### 
def cls():
    global img_text

    # Imageを初期化
    img_text =  Image.new("RGB", (SCREEN_WIDTH * 8, SCREEN_HEIGHT * 8), (0x00, 0x00, 0x00))


############################################################################### 
# 指定されたパスの画像をロードして2倍に拡大したImageを返却する
# 引数		filepath 画像データのフルパス
# 戻り値	2倍に拡大したImageデータ
############################################################################### 
def loadImage(filePath):

	img = Image.open(filePath).convert("RGBA")
	return img


############################################################################### 
# テキスト座標系からグラフィック座標系に変換する
# 引数      value 変換する値
# 戻り値    変換後の値
############################################################################### 
def gPos(value):

	return value * 8


# Windowを生成
root = tkinter.Tk()
root.geometry(str(SCREEN_WIDTH * 8 * 2) + "x" + str(SCREEN_HEIGHT * 8 * 2))
root.title("HEART CATCH HARUMI-CHAN on python")
root.bind("<KeyPress>", pressKey)
root.bind("<KeyRelease>", releaseKey)

# Canvas生成
canvas = tkinter.Canvas(width = (SCREEN_WIDTH * 8 * 2), height = (SCREEN_HEIGHT * 8 * 2))
canvas.pack()

# はるみちゃん（タイトル）
img_harumi00 = loadImage(basePath + os.sep + "Images" + os.sep + "harumi_00.png")

# YOU
img_you = (
    loadImage(basePath + os.sep + "Images" + os.sep + "you_00.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_01.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_04.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_02.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_03.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_05.png"),
    loadImage(basePath + os.sep + "Images" + os.sep + "you_06.png")
)

# フォントイメージ
img_fonts = loadImage(basePath + os.sep + "Images" + os.sep + "p8font.png")
img_font = []
img_font_mask = []
for h in range(0, img_fonts.height, 8):
    for w in range(0, img_fonts.width, 8):
        img = img_fonts.crop((w , h, w + 8, h + 8))
        # フォント画像生成
        img_font.append(img)
        # マスク画像生成
        img_font_mask.append(ImageOps.invert(img.convert("L")))

# プテラノドンのキャラクタ定義
ptera = (
    ( (0x20, 0x20, 0x20, 0x20, 0x20), (0x2E) ),
    ( (0x94, 0xEF, 0x5E, 0xEE, 0x94), (0x56) ),
    ( (0xEE, 0xEF, 0x5E, 0xEE, 0xEF), (0x56) )
)

# テキスト画面のImage初期化
cls()

# メイン処理
main()

# ウィンドウイベントループ実行
root.mainloop()
