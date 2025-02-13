# -*- coding: utf-8 -*-
import sys
import io
import json
from rapidocr_onnxruntime import RapidOCR

# 设置 Python 的输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 初始化 RapidOCR 并将其设置为全局变量
engine = RapidOCR()

def main(image_path):
    # 进行图片识别
    result, elapse = engine(image_path)

    # 创建一个字典来存储结果和处理时间
    output_data = {
        "recognition_result": result,
        "processing_time": elapse
    }

    # 将结果转换为 JSON 格式
    output_json = json.dumps(output_data, ensure_ascii=False, indent=4)

    # 打印 JSON 格式的结果
    print(output_json)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python RapidOCR.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    main(image_path)