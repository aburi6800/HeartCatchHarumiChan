import os
from PIL import Image, ImageTk, ImageDraw, ImageOps

############################################################################### 
# キャラクタ画像生成プログラム
############################################################################### 

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

# キャラクタサイズ
VRM_WIDTH = 3
VRM_HEIGHT = 4

# スクリプトのパス
basePath = os.path.abspath(os.path.dirname(__file__))


############################################################################### 
# テキスト描画
# 引数		img 貼り付け先のImageデータ
#  			x テキスト座標系のx座標
#			y テキスト座標系のy座標
#			s 表示する文字データの配列（文字の場合は、文字コードに対応した文字を表示する）
#           c 文字の表示色（省略時は白）
############################################################################### 
def writeText(img, x, y, s, c=COLOR_7):

    if type(s) is int:
        s = [s]

    # 指定色で塗りつぶした矩形を作成
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


# イメージをロード
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

# はるみちゃん（タイトル用）
offScreen = Image.new("RGBA", (gPos(3), gPos(5)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x20, 0x20), COLOR_3)
writeText(offScreen, 0, 1, (0x97, 0xED, 0x88), COLOR_3)
writeText(offScreen, 0, 2, (0x20, 0x87, 0x20), COLOR_3)
writeText(offScreen, 0, 3, (0xE4, 0x86, 0xE5), COLOR_3)
writeText(offScreen, 0, 4, (0xEE, 0x96, 0x20), COLOR_3)
#offScreen.save(basePath + os.sep + "Images" + os.sep + "harumi_00.png")


# YOU（タイトル用）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9E, 0x95, 0x9D, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0x20, 0x3F, 0x96, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x97, 0xEE, 0x86, 0xEF, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x20, 0x86, 0x97, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0xEE, 0x20, 0x88, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x88, 0x20, 0x88, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_00.png")

# YOU（左）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9E, 0x95, 0x9D, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0x20, 0x3F, 0x96, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0xEE, 0x86, 0xEF, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x88, 0x86, 0x97, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0xEE, 0x20, 0x88, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x88, 0x20, 0x88, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_01.png")

# YOU（左：投げる１）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x97, 0x9E, 0x95, 0x9D, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0xEF, 0x3F, 0x96, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0x20, 0x86, 0xEF, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x20, 0x86, 0x97, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0xEE, 0x20, 0x88, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x88, 0x20, 0x88, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_02.png")


# YOU（左：投げる２）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9E, 0x95, 0x9D, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x94, 0xEF, 0x3F, 0x96, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0x20, 0x86, 0xEF, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x20, 0x86, 0x97, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0xEE, 0x20, 0x88, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x88, 0x20, 0x88, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_03.png")


# YOU（右）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9C, 0x95, 0x9F, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0x96, 0x3F, 0x20, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0xEE, 0x86, 0xEF, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x88, 0x86, 0x97, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0x97, 0x20, 0xEF, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x97, 0x20, 0x97, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_04.png")


# YOU（右：投げる１）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9C, 0x95, 0x9F, 0x88), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0x96, 0x3F, 0xEE, 0x20), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0xEE, 0x86, 0x20, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x88, 0x86, 0x20, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0x97, 0x20, 0xEF, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x97, 0x20, 0x97, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_05.png")


# YOU（右：投げる２）
offScreen = Image.new("RGBA", (gPos(5), gPos(6)), (0, 0, 0))
writeText(offScreen, 0, 0, (0x20, 0x9C, 0x95, 0x9F, 0x20), COLOR_7)
writeText(offScreen, 0, 1, (0x20, 0x96, 0x3F, 0xEE, 0x94), COLOR_7)
writeText(offScreen, 0, 2, (0x20, 0xEE, 0x86, 0x20, 0x20), COLOR_7)
writeText(offScreen, 0, 3, (0x20, 0x88, 0x86, 0x20, 0x20), COLOR_7)
writeText(offScreen, 0, 4, (0x20, 0x97, 0x20, 0xEF, 0x20), COLOR_1)
writeText(offScreen, 0, 5, (0x20, 0x97, 0x20, 0x97, 0x20), COLOR_1)

writeText(offScreen, 2, 2, (0x86), COLOR_6)
writeText(offScreen, 2, 3, (0x86), COLOR_6)

offScreen.save(basePath + os.sep + "Images" + os.sep + "you_06.png")
