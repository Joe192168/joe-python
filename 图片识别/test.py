import os
from fastapi import FastAPI, File, UploadFile
from paddleocr import PaddleOCR
import uvicorn
from typing import List
from PIL import Image
import numpy as np
 
# 初始化 PaddleOCR
ocr = PaddleOCR(lang='ch')
 
# 创建 FastAPI 实例
app = FastAPI()
 
# 定义 OCR 接口
@app.post("/ocrImages")
async def perform_ocr(images: List[UploadFile] = File(...)):
    # 获取环境变量 OCR_NEWLINE，默认为 False
    newline_flag = os.getenv("OCR_NEWLINE", "false").lower() == "true"
    results = ""
    for file in images:
        contents = await file.read()
        # 将图像保存到临时文件并执行 OCR
        with open(f"/tmp/{file.filename}", "wb") as f:
            f.write(contents)
        # 调整图像大小
        image = Image.open(f"/tmp/{file.filename}")
        image = image.resize((1280, 720), Image.LANCZOS)
 
        # 将 PIL 图像转换为 NumPy 数组
        image_np = np.array(image)
        result = ocr.ocr(image_np, cls=True)
        # 保存识别结果
        for line in result:
            for word_info in line:
                text = word_info[1][0]
                if newline_flag:
                    results += text + "\n"  # 使用换行符
                else:
                    results += text + " "
    return {"ocr_text": results}
 
# 主函数，运行 API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6012)