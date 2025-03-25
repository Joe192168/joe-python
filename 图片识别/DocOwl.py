from docowl_infer import DocOwlInfer

# 加载模型
model_path = './mPLUG/DocOwl1.5-stage1'
docowl = DocOwlInfer(ckpt_path=model_path, anchors='grid_9', add_global_img=False)
print('load model from ', model_path)

# 文档/网页解析
image = './DocStruct4M/val_imgs/CCpdf/pages/1e531ef22cff3f01dab8720e99427c4f_page19.png'
query = 'Recognize text in the image.'
answer = docowl.inference(image, query)
print(answer)

# 表格/图表转Markdown
image = './DocStruct4M/val_imgs/TURL/col_type_197091.jpg'
query = 'Convert the picture to Markdown syntax.'
answer = docowl.inference(image, query)
print(answer)

# 自然图像解析
image = './DocStruct4M/val_imgs/OCRCC/02749938.jpg'
query = 'Provide a description of the image content and text.'
answer = docowl.inference(image, query)
print(answer)