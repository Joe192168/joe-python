# 使用 Python 基础镜像
FROM python:3.12-slim
 
# 设置工作目录
WORKDIR /app
 
# 安装系统依赖（包括 git 和编译工具等）
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
 
# 安装 PaddleOCR 所需的依赖包
COPY requirements.txt .
 
RUN pip install --no-cache-dir -r requirements.txt
 
# 复制应用程序代码
COPY . .
 
# 暴露 API 服务端口
EXPOSE 6012
 
# 启动 FastAPI 应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6012"]