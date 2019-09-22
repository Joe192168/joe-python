import os
from PIL import Image

os.chdir(r"E:\pic")
os.getcwd()
img = Image.open(r"xhq.jpg")

print(f"图像格式：{img.format}")
print(f"图像尺寸：{img.size}")
print(f"图像模式：{img.mode}")
#从缓存中显示
img.show()
img.save("xhq_bak.png","PNG")

#改变图片尺寸
size = (120,120)
img.thumbnail(size)
img.show()
img.save("xhq_thumbnail.jpg","PNG")

#变成黑白
out4 = img.convert("L")
out4.show()
out4.save("xhq_hb.jpg","PNG")