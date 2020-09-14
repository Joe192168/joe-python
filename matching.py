#-*- coding:utf-8 -*-
import re
import jieba
import time
import datetime
import xlrd,xlwt
import logging
import Levenshtein

#log日志
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#全局字典
data = []

#设置单元格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle() # 初始化样式

    font = xlwt.Font() # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


#写入excel文件
def write_excel(url, data): #传入文件存储路径、excel的sheet名称、以及要插入的数据
    try:
        #data = (('biqi', 963, 177), ('editor_Intern1', 912, 154), ('editor_Intern10', 840, 163), ('editor_Intern11', 644, 173)) #模板数据
        myWorkbook = xlwt.Workbook(encoding="utf-8") #创建excel
        #创建第一个sheet
        sheet1 = myWorkbook.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
        row0 = [u'品名A',u'产地A',u'规格A',u'品名B',u'产地B',u'规格B']
        #生成第一行
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

        for i, val in enumerate(data):
            for j, value in enumerate(val):
                sheet1.write(i+1, j, value) #遍历数据插入sheet中
        myWorkbook.save(url) #将创建的excel保存在该路径下
    except:
        logging.exception('write_excel exception：')

def checkText(file_dir,kh_mc,kh_cd,kh_gg,mc_xsd,cd_xsd,gg_xsd):
    try:
        wb = xlrd.open_workbook(file_dir) #打开excel表
        #获取所有sheet工作簿名称
        sheets = wb.sheet_names()
        for item in sheets:
            #通过名字获取某个sheet页的值
            sheet = wb.sheet_by_name(item)
            #获取行数
            nrows = sheet.nrows
            #获取总列数
            #ncols = sheet.ncols
            #print("The sum rows:%d" %nrows)
            #print("The sum cols:%d" %ncols)

            #获取列数
            for i in range(1,nrows):
                # 从第二行开始匹配
                #产品名称
                mb_cp = str(sheet.cell_value(i,0)).strip();
                #产地名称
                mb_cd = str(sheet.cell_value(i,1)).strip();
                #规格
                mb_gg = str(sheet.cell_value(i,2)).strip();
                #print('queryText:'+queryText+'\tcp_a:'+cp_a)
                #产品名称
                a = acquaintance(mb_cp,kh_mc)
                if a >= float(mc_xsd):
                    ret_mc = True
                else:
                    ret_mc = False
                #产地
                b = acquaintance(mb_cd,kh_cd)
                if b >= float(cd_xsd):
                    ret_cd = True
                else:
                    ret_cd = False
                #规格
                c = jaccrad(mb_gg,kh_gg)
                if c >= float(gg_xsd):
                    ret_gg = True
                else:
                    ret_gg = False
                if ret_mc and ret_cd and ret_gg:
                    print('根据相似度匹配成功的品名：'+mb_cp+'\t产地：'+mb_cd+'\t规格：'+mb_gg)
                    #print('客户数据品牌名：'+_mc+'\t客户数据产地：'+_cd+'\t客户数据规格：'+_gg)
                    data_dict = []
                    data_dict.append(kh_mc)
                    data_dict.append(kh_cd)
                    data_dict.append(kh_gg)
                    data_dict.append(mb_cp)
                    data_dict.append(mb_cd)
                    data_dict.append(mb_gg)
                    data.append(data_dict)

    except:
        logging.exception('checkText exception：')

#根据文件夹 截取文件名称
def getFileList(path_a,path_b,mc_xsd,cd_xsd,gg_xsd):
    try:
        #获取excel文件内容，并判断是否包含
        wb = xlrd.open_workbook(path_a) #打开excel表
        #获取所有sheet工作簿名称
        sheets = wb.sheet_names()
        for item in sheets:
            #通过名字获取某个sheet页的值
            sheet = wb.sheet_by_name(item)
            #获取行数
            nrows = sheet.nrows
            for i in range(1,nrows):
                #产品名称
                cp = str(sheet.cell_value(i,0)).strip();
                #产地名称
                cd = str(sheet.cell_value(i,1)).strip();
                #规格
                gg = str(sheet.cell_value(i,2)).strip();
                checkText(path_b,cp,cd,gg,mc_xsd,cd_xsd,gg_xsd)
    except:
        logging.exception('getFileList exception：')

#计算相似度算法
def acquaintance(a,b):
    return Levenshtein.ratio(a,b)

# 计算jaccard系数
def jaccrad(model, reference):  # terms_reference为源句子，terms_model为候选句子
    #jieba.set_dictionary("dict.txt")
    #jieba.initialize()
    terms_reference = jieba.cut(reference,cut_all=True)  # 默认精准模式
    terms_model = jieba.cut(model)
    grams_reference = set(terms_reference)  # 去重；如果不需要就改为list
    grams_model = set(terms_model)
    temp = 0
    for i in grams_reference:
        if i in grams_model:
            temp = temp + 1
    fenmu = len(grams_model) + len(grams_reference) - temp  # 并集
    jaccard_coefficient = float(temp / fenmu)  # 交集
    return jaccard_coefficient

if __name__ == '__main__':
    mc_xsd = input("品名相似度(如：0-1之间，0.6相当于百分之60的概率)：")
    cd_xsd = input("产地相似度(如：0-1之间，0.6相当于百分之60的概率)：")
    gg_xsd = input("规格相似度(如：0-1之间，0.6相当于百分之60的概率)：")
    #不接受09这样的为整数
    regInt='^0$|^[1-9]\d*$'
    #接受0.00、0.360这样的为小数，不接受00.36，思路:若整数位为零,小数位可为任意整数，但小数位数至少为1位，若整数位为自然数打头，后面可添加任意多个整数，小数位至少1位
    regFloat='^0\.\d+$|^[1-9]\d*\.\d+$'
    regIntOrFloat=regInt+'|'+regFloat#整数或小数
    patternIntOrFloat=re.compile(regIntOrFloat)#创建pattern对象，以便后续可以复用
    if patternIntOrFloat.search(mc_xsd) or patternIntOrFloat.search(cd_xsd) or patternIntOrFloat.search(gg_xsd):
        path_a = input("请输入客户数据的excel文件路径(如：C:/A.xlsx)：")
        path_b = input("请输入目录表的excel文件路径(如：C:/B.xlsx)：")
        start = time.time()
        #匹配数据字典
        getFileList(path_a,path_b,mc_xsd,cd_xsd,gg_xsd)
        # 获取当前时间
        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 判断字典是否非空
        if data:
            #导出exlce结果
            write_excel('匹配结果_'+nowTime+'.xls',data)
            print("匹配完成，并保存完毕")
        else:
            print("没有匹配的数据，请重新检查")
        end = time.time()
        print("耗时: %.3fs" % (end - start))
    else:
        print("输入的相似度不是数字，请重新输入")