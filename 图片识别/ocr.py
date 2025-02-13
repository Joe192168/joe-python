import json
from paddleocr import PaddleOCR, draw_ocr
import cv2
from PIL import Image

# 初始化OCR模型，选择使用的语言（这里以中文和英文为例）
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 需要识别其他语言时，可以在lang参数中添加

# 读取图片
img_path = 'e:/Git/joe-python/图片识别/5.jpg'  # 替换为你的图片路径
img = cv2.imread(img_path)

# 使用OCR模型识别图片中的文本
result = ocr.ocr(img_path, cls=True)

# 处理识别结果，转换为JSON格式
json_result = {
    "image_path": img_path,
    "results": []
}

for line in result:
    line_info = {
        "bbox": line[0],  # 边界框坐标
        "text": line[1][0],  # 识别的文本
        "score": line[1][1]  # 置信度
    }
    if len(line) > 2 and line[2] is not None:
        line_info["direction"] = line[2][0]  # 文字方向（如果有方向分类器）
    json_result["results"].append(line_info)

# 将结果转换为JSON字符串（如果需要保存到文件，可以使用json.dump）
json_str = json.dumps(json_result, indent=4, ensure_ascii=False)
print(json_str)

# 如果需要，可以将结果保存到JSON文件中
# with open('ocr_result.json', 'w', encoding='utf-8') as f:
#     f.write(json_str)