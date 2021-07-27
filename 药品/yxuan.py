import time
import math
import difflib
import Levenshtein
from jieba import posseg

# 对要进行比较的str1和str2进行计算，并返回相似度
def simicos(str1, str2):
    # 对两个要计算的字符串进行分词, 使用隐马尔科夫模型(也可不用)
    # 由于不同的分词算法, 所以分出来的结果可能不一样
    # 也会导致相似度会有所误差, 但是一般影响不大
    # 如果想把所有的词性都计算，那么把if及其后面的全部删除掉即可
    cut_str1 = [w for w, t in posseg.lcut(str1) if 'n' in t or 'v' in t]
    cut_str2 = [w for w, t in posseg.lcut(str2) if 'n' in t or 'v' in t]
    # 列出所有词
    all_words = set(cut_str1 + cut_str2)
    # 计算词频
    freq_str1 = [cut_str1.count(x) for x in all_words]
    freq_str2 = [cut_str2.count(x) for x in all_words]
    # 计算相似度
    sum_all = sum(map(lambda z, y: z * y, freq_str1, freq_str2))
    sqrt_str1 = math.sqrt(sum(x ** 2 for x in freq_str1))
    sqrt_str2 = math.sqrt(sum(x ** 2 for x in freq_str2))
    return sum_all / (sqrt_str1 * sqrt_str2)

def get_equal_rate(str1, str2):
    return Levenshtein.jaro_winkler(str1, str2)

def acquaintance(a,b):
    return Levenshtein.ratio(a,b)

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

#过滤词，这里只是针对不同网站标题的过滤词，如果数量很大可以保存在一个文件中
stopwords = ["【","】","[","]","直邮","包邮","保税","全球购","包税","（","）","原装","京东超市","马尾保税仓","发货","进口","+","/","-","亏本","特价","现货","天天特价","专柜","代购","预定","正品","旗舰店","#",
             "转卖","国内","柜台","无盒","保税仓","官方","店铺","爆款","、"]

#停用词，这里只是针对例子增加的停用词，如果数量很大可以保存在一个文件中
conversions = ["T","片","支","粒","袋","丸","瓶","mg","m","g","ml"]

    #返回原始字符串分词后和对比字符串的匹配次数，返回一个字典
def Compared(self,str_list):
    dict_data={}
    # sarticiple =list(jieba.cut(self.word.strip()))
    for cons in conversions:
        self.word[4] = self.word[4].replace(cons, "")
        # print(self.word[4])
    sarticiple = [self.word[0],self.word[2],self.word[3],self.word[4],self.word[5],self.word[6],self.word[7]]
    for strs in str_list:
        for sws in stopwords:
            strs_1 = strs.replace(sws.decode("utf-8")," ")
        num=0
        for sart in sarticiple:
            # print("qqqqqqqqqqqqqqq",sart.decode("utf-8"))
            sart = sart.decode("utf-8")
            counts = strs_1.count(sart)
            # print("zzzzzzzzzzzzzzzzzzz",strs_1)
            if counts!=0:
                # print("=========",sart)
                num = num+1
            else:
                # print("..............", sart)
                num = num-100
        if num>0:
            dict_data[strs]=num
    return dict_data

if __name__ == '__main__':
    case1 = "50mg*10片"
    case2 = "50mg*1片"
    case3 = '50mg*10片'
    case4 = '50mg*1片'
    case5 = "一车主为防碰瓷，将玛莎拉蒂布满玻璃渣，网友惊呼：绝了！"
    case6 = "车主为保护玛莎拉蒂将其布满玻璃渣，防“碰瓷”也是绝了！"
    case7 = "10片"
    case8 = "1片"
    a = ["你好",'hello,world','计算偏差大不大啊？','文本可以吗','请看这里']
    b = ['helloworld',"你好吗？",'可以吗','请这里','计算偏差大不大']
    start = time.time()
    #similarity = simicos(case1, case2)
    similarity1 = get_equal_rate(case1, case2)
    similarity2 = acquaintance(case1,case2)
    end = time.time()
    print("耗时: %.3fs" % (end - start))
    print("相似度1: %.3f" % similarity1)
    print("相似度2: %.3f" % similarity2)
    print("difflib相似度：%.3f" % string_similar(case1,case2))