# 给去除了背景的图像添加背景颜色
from PIL import Image
from PIL import ImageColor

# 输入已经去除背景的图像
im = Image.open('pictrue/20190822142124.png_no_bg.png')
x, y = im.size

pic_colour = input("如：blue 蓝色,red 红色,white 白色 请输入背景颜色：")

try:
    #颜色转换16进制
    pic_rgb = ImageColor.getcolor(pic_colour, "RGB")
    # 填充红色背景
    p = Image.new("RGBA", im.size, pic_rgb)
    p.paste(im, (0, 0, x, y), im)
    # 保存填充后的图片
    p.save('pictrue/Joy_red_bg.png')
except:
    with open('/error.log', 'a') as f:
        f.write('background change fail .')