# python3
import urllib.request
import urllib.parse
import json
import time
import base64
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd

# 定义图片字典
image_dict = {}
# 定义图片转码结合
img_base64_list = []

# 用户选则上传图片
def select_images():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # 定义上传文件类型
    file_types = [('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.jpg')]
    selected_files = filedialog.askopenfilenames(title="选择图片", filetypes=file_types)
    for file in selected_files:
        if os.path.exists(file) and os.path.isfile(file):
            print(f"选择了有效的图片: {file}")
            # 获取路径中的文件名
            file_name_extension = os.path.basename(file)
            # 图片转码
            image_base64 = handleImgBase64(file)
            # 使用os.path.splitext()分离文件名和扩展名
            file_name, file_extension = os.path.splitext(file_name_extension)
            # 组装json
            image_dict[file_name] = image_base64
        else:
            print(f"路径 {file} 无效或不是指向一个文件")
    return image_dict

# 处理图片转码
def handleImgBase64(image_info):
    with open(image_info, 'rb') as f:  # 以二进制读取本地图片
        data = f.read()
        encodestr = str(base64.b64encode(data), 'utf-8')
    return encodestr

# 请求头
headers = {
    'Authorization': 'APPCODE 8c203286e5e94ec19aef9c38531ebe42',
    'Content-Type': 'application/json; charset=UTF-8'
}

# 请求ocr
def posturl(url,data={}):
    try:
        params = json.dumps(dict).encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html = r.read()
        r.close();
        return html.decode("utf8")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    time.sleep(1)

if __name__=="__main__":
    url_request = "https://ocrapi-document.taobao.com/ocrservice/document"
    # 选中图片
    json_data = select_images()
    # 使用ExcelWriter创建或打开一个Excel文件
    with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='w') as writer:
        for sheet_name, data_image in json_data.items():
            print(f'正在处理文件名称：{sheet_name}...')
            dict = {'img': data_image}
            json_data = posturl(url_request, data=dict)
            # 解析 JSON 数据
            parsed_data = json.loads(json_data)
            # 提取需要的部分并重新组装成新的JSON结构
            new_parsed_data = [{"word": info["word"]} for info in parsed_data["prism_wordsInfo"]]
            # 将数据转换为pandas DataFrame
            df = pd.DataFrame(new_parsed_data)
            # 将DataFrame写入Excel文件的第一个工作表
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Excel文件 'output.xlsx' 已创建或更新，每个集合作为一个单独的工作表。")