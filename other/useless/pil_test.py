from PIL import Image, ImageDraw, ImageFont
import sys
import PIL
im = Image.open("/home/basdk/Desktop/map.png")
draw = ImageDraw.Draw(im)
for i in range(11):
    draw.line((im.size[0]*i/10, 0, im.size[0]*i/10, im.size[1]), fill=0)

for i in range(11):
    draw.line((0, im.size[1]*i/10, im.size[0], im.size[1]*i/10), fill=0)
arial = ImageFont.truetype("/usr/share/fonts/noto/NotoSansTaiLe-Regular.ttf",size=50)
draw.text((0, 0), "A", (0, 0, 0), font=arial)
del draw

im.show()
