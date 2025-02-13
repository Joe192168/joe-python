import easyocr

# 创建一个 EasyOCR 读取器实例，指定需要识别的语言
reader = easyocr.Reader(['ch_sim', 'en'])  # ch_sim 表示简体中文，en 表示英文

# 读取图像文件，并调用 read 方法进行文字识别
result = reader.readtext('d:/5.jpg')  # 替换为你的图片路径

# 打印识别结果
for (bbox, text, prob) in result:
    print(f"Detected text: {text}, Confidence: {prob:.2f}")