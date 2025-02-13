from paddleocr import PaddleOCR
import json

def ocr_image_to_json(image_path):
    # 初始化PaddleOCR实例（使用中英文模型）
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # lang可选：ch（中文）、en（英文）等
    
    try:
        # 执行OCR识别
        result = ocr.ocr(image_path, cls=True)
        
        # 解析识别结果
        ocr_results = []
        for idx, line in enumerate(result):
            if line:  # 检查是否存在有效识别结果
                for item in line:
                    position = item[0]   # 文字位置坐标
                    text = item[1][0]     # 识别文本
                    confidence = item[1][1]  # 置信度
                    
                    ocr_results.append({
                        "index": idx,
                        "position": [[round(p[0], 2), round(p[1], 2)] for p in position],  # 保留两位小数
                        "text": text,
                        "confidence": round(float(confidence), 4)  # 转换为float并保留4位小数
                    })

        # 转换为JSON格式
        json_output = json.dumps({
            "status": "success",
            "data": ocr_results
        }, ensure_ascii=False, indent=2)  # 禁用ASCII转义以正确显示中文

        return json_output

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    image_path = "e:/Git/joe-python/图片识别/5.jpg"  # 替换为你的图片路径
    result_json = ocr_image_to_json(image_path)
    print(result_json)