from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
import uvicorn
from typing import List
from PIL import Image
import numpy as np
import io
import logging
import os

# 根据选择的方案修改以下导入
# 方案一使用：
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
# 方案二使用：
# from pydantic import BaseSettings

class Settings(BaseSettings):
    ocr_newline: bool = False
    model_dir: str = "./models"
    image_resize: tuple = (1280, 720)

    # 方案一配置
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="OCR_"
    )
    
    # 方案二配置（保持原样）
    # class Config:
    #     env_file = ".env"
    #     env_prefix = "OCR_"

settings = Settings()

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(
            lang='ch',
            det_model_dir=os.path.join(settings.model_dir, "ch_PP-OCRv4_det_infer"),
            rec_model_dir=os.path.join(settings.model_dir, "ch_PP-OCRv4_rec_infer"),
            use_angle_cls=False,
            show_log=False
        )

    async def process_image(self, image_data: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = image.resize(settings.image_resize, Image.LANCZOS)
            return self._format_result(self.ocr.ocr(np.array(image), cls=True))
        except Exception as e:
            logging.error(f"Image processing error: {str(e)}")
            raise

    def _format_result(self, result: list) -> str:
        return ("\n" if settings.ocr_newline else " ").join(
            word_info[1][0] for line in result for word_info in line
        )

app = FastAPI()
ocr_processor = OCRProcessor()

@app.post("/ocrImages")
async def perform_ocr(images: List[UploadFile] = File(...)):
    try:
        # 初始化结果容器
        all_texts = []
        
        # 遍历处理每张图片
        for file in images:
            if not file.content_type.startswith('image/'):
                raise HTTPException(400, f"文件 {file.filename} 不是图片类型")
            
            # 内存处理图像
            image_data = await file.read()
            text = await ocr_processor.process_image(image_data)
            
            # 添加带换行的结果
            all_texts.append(f"{text}")  # 文件名作为注释
            
        # 全量文本用双换行分隔
        full_text = "\n".join(all_texts)
        
        return {"ocr_text": full_text}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"处理失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6012)