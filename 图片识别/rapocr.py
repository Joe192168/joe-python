import json
from rapidocr_onnxruntime import RapidOCR

# 初始化 RapidOCR，确保只加载一次
engine = RapidOCR(use_gpu=True)  # 如果支持 GPU，设置 use_gpu=True

def recognize_image(img_path):
    # 进行图片识别
    result, elapse = engine(img_path)

    # 创建一个字典来存储结果和处理时间
    output_data = {
        "recognition_result": result,
        "processing_time": elapse
    }

    # 将结果转换为 JSON 格式
    output_json = json.dumps(output_data, ensure_ascii=False, indent=4)

    # 返回 JSON 格式的结果
    return output_json

# 图片路径
img_path = 'e:/Git/joe-python/图片识别/5.jpg'

# 调用识别函数
output_json = recognize_image(img_path)

# 打印 JSON 格式的结果
print(output_json)