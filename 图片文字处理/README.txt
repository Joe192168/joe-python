打包为单个可执行文件：
img-ocr.py

设置输出文件名和输出目录
--name=imag_ocr

添加图标（需要一个.ico文件）
--icon=sb.ico

隐藏控制台窗口（适用于GUI应用）
--windowed

打包命令
pyinstaller --onefile --windowed --icon=sb.ico --name=imag_ocr img-ocr.py