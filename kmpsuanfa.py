import jieba
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

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

def KMP_algorithm(string, substring):
    '''
    KMP字符串匹配的主函数
    若存在字串返回字串在字符串中开始的位置下标，或者返回-1
    '''
    pnext = gen_pnext(substring)
    n = len(string)
    m = len(substring)
    i, j = 0, 0
    while (i<n) and (j<m):
        if (string[i]==substring[j]):
            i += 1
            j += 1
        elif (j!=0):
            j = pnext[j-1]
        else:
            i += 1
    if (j == m):
        return i-j
    else:
        return -1


def gen_pnext(substring):
    """
    构造临时数组pnext
    """
    index, m = 0, len(substring)
    pnext = [0]*m
    i = 1
    while i < m:
        if (substring[i] == substring[index]):
            pnext[i] = index + 1
            index += 1
            i += 1
        elif (index!=0):
            index = pnext[index-1]
        else:
            pnext[i] = 0
            i += 1
    return pnext

if __name__ == "__main__":
    string = '25mg*20片'.lower()
    substring = '25mg*20片/瓶'.lower()
    out = KMP_algorithm(string, substring)
    print(out)
    a = '10ml*6'.lower()
    b = '10ml*5支'.lower()
    # out = fuzz.token_sort_ratio(a, b)
    # print(out)
    # g = process.extractOne(a, b)
    # print(g)
    # c = jaccrad(a,b)
    # print(c)
    d = Levenshtein.ratio(a,b)
    print(d)
    if d>float(0.78):
        print('正确')