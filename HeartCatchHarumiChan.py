import time
import tkinter
import random
import os
import csv
import numpy
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageChops

############################################################################### 
# 初期処理
############################################################################### 

# 仮想VRAMのサイズ
VRM_WIDTH = 40
VRM_HEIGHT = 25

# ゲームの状態
GAMESTATUS_TITLE = 0
GAMESTATUS_START = 1
GAMESTATUS_GAME = 2
GAMESTATUS_MISS = 3
GAMESTATUS_GOAL = 4
GAMESTATUS_OVER = 5

# キー判定用
KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_SPACE = "space"
KEY_Z = "z"

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

# 空の仮想VRAM配列
blankRow = [0] * VRM_WIDTH
vrm = [blankRow] * VRM_HEIGHT

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

# プテラノドンの座標
ptera_x = 25
ptera_y = 16
ptera_old_x = 0
ptera_old_y = 0
ptera_direction = 1


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

#    else:
#        # ゲームメイン処理
#       game()		

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
    global key

#    if key == KEY_SPACE:
#        # ゲーム初期化
#        initializeGame()
#        changeGameStatus(GAMESTATUS_GAME)

    key = ""


############################################################################### 
# ゲーム初期化
############################################################################### 
def initializeGame():

    pass


############################################################################### 
# ラウンド初期化
############################################################################### 
def initializeRound():

    pass


############################################################################### 
# ゲーム処理
############################################################################### 
def game():
    global key, ptera_direction, ptera_x, ptera_y, ptera_old_x, ptera_old_y

    # テスト：プテラノドンを動かす
    ptera_old_x = ptera_x
    ptera_old_y = ptera_y
    ptera_direction = 1 - ptera_direction
    ptera_y = ptera_y + ptera_direction * -(random.randint(0, 5) < 4)
    if ptera_x > 13 and ptera_x < 33:
        ptera_x = ptera_x + (random.randint(0, 2) - 1)

#    if key == KEY_SPACE:
#        # ゲーム初期化
#        initializeGame()
#        changeGameStatus(GAMESTATUS_GAME)

    key = ""


############################################################################### 
# 画面描画
############################################################################### 
def draw():
    global photoImage, flash1_flg

    # canvasのイメージ削除
    canvas.delete("SCREEN")

    if gameStatus == GAMESTATUS_TITLE:
        # タイトル
        drawTitle()

#    else:
#        # ゲーム画面
#        img_screen = drawGame()

    # 画面表示用イメージ生成
    img_screen = img_text.copy()

    # フラッシュ１処理
    # うまくいってない
    if flash1_flg:
        flash1_flg = False
        plane = img_screen.split()
        _r = plane[0].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        _g = plane[1].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        _b = plane[2].point(lambda _: 0x01 if _ > 0x01 else 0x00, mode = "1")
        img_mask = ImageChops.logical_and(_r, _g)
        img_mask = ImageChops.logical_and(img_mask, _b)
        img_screen.paste(Image.new("RGB", img_text.size, (255, 255, 255)), mask = img_mask)

    # 画面イメージを拡大
    img_screen = img_text.resize((img_screen.width * 2, img_screen.height * 2), Image.NEAREST)

    # オフスクリーンでPhotoImage生成
    photoImage = ImageTk.PhotoImage(img_screen)
    canvas.create_image((img_screen.width / 2, img_screen.height / 2), image = photoImage, tag = "SCREEN")


############################################################################### 
# タイトル画面描画
############################################################################### 
def drawTitle():
    global img_text, title_x, harumi_y, flash1_flg

    # 画面イメージ作成
    if gameTime == 1:
        cls()
        writeText(img_text, 0, 0, (0x97, 0x20, 0x88, 0x20, 0x20, 0x20, 0x97, 0x20, 0x20, 0x20, 0x20, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x80, 0x80, 0xEE), COLOR_2)
        writeText(img_text, 0, 1, (0x97, 0x20, 0x88, 0x95, 0x95, 0x95, 0x97, 0xEF, 0x20, 0x20, 0xE9, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x95, 0x8F, 0x95), COLOR_2)
        writeText(img_text, 0, 2, (0xEE, 0x20, 0xEF, 0x20, 0x20, 0x20, 0x97, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x96, 0x20, 0x20, 0xD4, 0x20, 0xC2, 0x20, 0x95, 0x9B, 0x20), COLOR_2)
        title_x = -1
        harumi_y = -1

    # フラッシュ
    if gameTime <= 8:
        if gameTime % 2 == 0:
            flash1_flg = True

    # タイトル文字移動
    if gameTime >= 10 and gameTime <= 38:
        if gameTime == 10:
            title_x = 28
        writeText(img_text, title_x, 3, (0x20, 0x20, 0xEF, 0xED, 0x80, 0x20), COLOR_3)
        writeText(img_text, title_x, 4, (0x20, 0x20, 0x20, 0x87, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x97, 0x20, 0x88, 0x20, 0x97, 0x97, 0x20, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x80, 0x80, 0xEE, 0x20, 0x20, 0x20, 0x95, 0x20, 0x97, 0x20), COLOR_3)
        writeText(img_text, title_x, 5, (0x9C, 0xE0, 0xE0, 0xEF, 0xEF, 0xE0, 0xE0, 0x9D, 0xE0, 0x20, 0x97, 0x20, 0x88, 0x20, 0x97, 0x97, 0x20, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x95, 0x8F, 0x95, 0x20, 0x20, 0x20, 0x20, 0x20, 0x97, 0x20), COLOR_3)
        writeText(img_text, title_x, 6, (0x9E, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0, 0x9F, 0xE0, 0x20, 0xEE, 0x20, 0xEF, 0x20, 0xEE, 0x97, 0xEE, 0x20, 0x94, 0xEF, 0x20, 0x20, 0x95, 0x9B, 0x20, 0x20, 0xD4, 0x20, 0x80, 0x80, 0xEE, 0x20), COLOR_3)
        title_x = (title_x - 1) if title_x > 0 else 0


    # ハルミチャン落下
    if gameTime >= 38 and gameTime <= 50:
        if gameTime == 38:
            harumi_y = 3
        img_text.paste(img_harumi00, (gPos(2), gPos(harumi_y)))
        harumi_y = (harumi_y + 1) if harumi_y < 16 else 15

    # タイトル
    if gameTime == 51:
        # UFO消去
        writeText(img_text,  0,  5, [0x20] * 9)
        writeText(img_text,  0,  6, [0x20] * 9)
        # プテラノドン
        writeText(img_text, 27, 15, ptera[1][0], COLOR_1)
        writeText(img_text, 29, 16, ptera[1][1], COLOR_1)
        # "プログラミング レッスン"
        writeText(img_text, 10,  9, (0x3D, 0x20, 0xCC, 0xDF, 0xDB, 0xB8, 0xDE, 0xD7, 0xD0, 0xDD, 0xB8, 0xDE, 0x20, 0xE9, 0x20, 0xDA, 0xAF, 0xBD, 0xDD, 0x20, 0x3D), COLOR_6) 
        # "ハルミチャン"
        writeText(img_text,  1, 21, (0xCA, 0xD9, 0xD0, 0xC1, 0xAC, 0xDD), COLOR_7)
        # "プテラノドン"
        writeText(img_text, 24, 21, (0xCC, 0xDF, 0xC3, 0xD7, 0xC9, 0xC4, 0xDE, 0xDD), COLOR_7)
        # "YOU!"
        writeText(img_text, 18, 18, (0x3C, 0x20, 0x59, 0x4F, 0x55, 0x20, 0x21), COLOR_7)
        # その他の表示
        writeText(img_text, 13, 21, (0x31, 0x20, 0x3C, 0x2D, 0x3E, 0x20, 0x33), COLOR_7)
        writeText(img_text, 10, 22, (0x42, 0x41, 0x4C, 0x4C, 0x20, 0x3D, 0x20, 0x53, 0x50, 0x41, 0x43, 0x45), COLOR_7)
        writeText(img_text, 13, 24, (0x50, 0x55, 0x53, 0x48, 0x20, 0x5B, 0x53, 0x5D, 0x20, 0x21), COLOR_7)


############################################################################### 
# ゲーム画面描画
############################################################################### 
def drawGame():
    global img_text

    # プテラノドン消去
    writeText(img_text, ptera_old_x    , ptera_old_y    , ptera[0][0], COLOR_1)
    writeText(img_text, ptera_old_x + 2, ptera_old_y + 1, ptera[0][1], COLOR_1)
    # プテラノドン描画
    writeText(img_text, ptera_x    , ptera_y    , ptera[ptera_direction + 1][0], COLOR_1)
    writeText(img_text, ptera_x + 2, ptera_y + 1, ptera[ptera_direction + 1][1], COLOR_1)


############################################################################### 
# テキスト描画
# 引数		img 貼り付け先のImageデータ
#  			x テキスト座標系のx座標
#			y テキスト座標系のy座標
#			s 表示する文字データの配列（文字の場合は、文字コードに対応した文字を表示する）
#           c 文字の表示色（省略時は白）
############################################################################### 
def writeText(img, x, y, s, c=COLOR_7):

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
    img.paste(imgBack, (gPos(x), gPos(y)), imgBack)


############################################################################### 
# テキスト画面クリア
############################################################################### 
def cls():
    global vrm, img_text

    # 仮想VRAM配列を初期化
    vrm = [blankRow] * VRM_HEIGHT

    # Imageを初期化
    img_text = img_text_blank


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
root.geometry(str(VRM_WIDTH * 8 * 2) + "x" + str(VRM_HEIGHT * 8 * 2))
root.title("HEART CATCH HARUMI-CHAN on ptera_ython")
root.bind("<KeyPress>", pressKey)
root.bind("<KeyRelease>", releaseKey)

# Canvas生成
canvas = tkinter.Canvas(width = (VRM_WIDTH * 8 * 2), height = (VRM_HEIGHT * 8 * 2))
canvas.pack()

# BG生成
img_text_blank = Image.new("RGBA", (VRM_WIDTH * 8, VRM_HEIGHT * 8), (0, 0, 0))

# テキスト画面のImage
img_text = img_text_blank

# はるみちゃん（タイトル）
img_harumi00 = loadImage(basePath + os.sep + "Images" + os.sep + "harumi_00.png")

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

# メイン処理
main()

# ウィンドウイベントループ実行
root.mainloop()
