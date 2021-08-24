from PIL import Image
import numpy as np
np.set_printoptions(threshold=np.inf)

im = Image.open('frog.jpg')
im = im.convert('RGBA')

# data是一个三维矩阵：长度 x 高度 x 4
# 其中的4是RGBA。A是Alpha的缩写，表示透明度
data = np.array(im)

# 切片取到RGBA各自的数组，为了方便下一步操作
red, green, blue, alpha = data.T

# 生成一个符合条件的布尔数组
white_areas = (red == 94) & (green == 175) & (blue == 55)

# 替换为想要的颜色
data[..., :-1][white_areas.T] = (255, 0, 0)

# 用操作好的数据生成图片
im2 = Image.fromarray(data)

# 保存图片
im2.save('red.png')