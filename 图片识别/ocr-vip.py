from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io
import logging
import asyncio

app = FastAPI(title="游戏截图OCR识别接口")
logger = logging.getLogger("uvicorn.error")

# 优化后的OCR引擎配置
ocr = PaddleOCR(
    lang='ch',
    use_angle_cls=True,
    use_gpu=False,  # 启用GPU加速
    det_limit_side_len=1600,  # 智能限制图像尺寸
    det_db_thresh=0.4,        # 平衡检测灵敏度
    det_db_box_thresh=0.6,
    rec_batch_num=30,          # 批量识别提升吞吐量
    enable_mkldnn=True        # CPU加速
)

async def async_ocr(img_array: np.ndarray):
    """异步OCR处理"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, 
        lambda: ocr.ocr(img_array, cls=True)
    )

def preprocess_image(img: Image.Image) -> np.ndarray:
    """智能图像预处理"""
    # 动态尺寸调整
    w, h = img.size
    if max(w, h) > 1600:
        scale = 1600 / max(w, h)
        img = img.resize((int(w*scale), int(h*scale)), Image.Resampling.LANCZOS)
    return np.array(img)

@app.post("/ocrImages")
async def process_game_screenshots(
    images: List[UploadFile] = File(...,description="上传游戏截图（支持PNG/JPG格式）")
):
    """优化版OCR接口（速度↑+准确率↑）"""
    results = []
    
    # 并行处理任务
    tasks = []
    for screenshot in images:
        # 文件验证
        if screenshot.content_type not in ["image/jpeg", "image/png"]:
            results.append({"filename": screenshot.filename, "error": "不支持的格式"})
            continue
        tasks.append(process_single_image(screenshot))
    
    # 并行执行
    results = await asyncio.gather(*tasks)
    return {"results": results}

async def process_single_image(screenshot: UploadFile):
    """单图片处理流程"""
    try:
        # 读取文件
        contents = await screenshot.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(413, detail="文件过大")
        
        # 预处理
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        img_array = preprocess_image(img)
        
        # OCR识别
        ocr_result = await async_ocr(img_array)
        
        # 结果过滤
        texts = []
        for page in ocr_result:
            if page:
                texts.extend(
                    line[1][0] 
                    for line in page 
                    if line[1][1] > 0.65  # 提高置信度阈值
                )
        
        return {
            "filename": screenshot.filename,
            "texts": texts,
            "warning": "检测到低精度内容" if len(texts)<3 else None
        }
    
    except Exception as e:
        logger.error(f"处理失败: {screenshot.filename} - {str(e)}")
        return {"filename": screenshot.filename, "error": "处理失败"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6012)