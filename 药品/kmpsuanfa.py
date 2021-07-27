import jieba
import datetime
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
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

def now():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def time_long(time1, time2, type="day"):
    """
    计算时间差
    :param time1: 较小的时间（datetime类型）
    :param time2: 较大的时间（datetime类型）
    :param type: 返回结果的时间类型（暂时就是返回相差天数）
    :return: 相差的天数
    """
    day1 = time.strptime(str(time1), '%Y-%m-%d')
    day2 = time.strptime(str(time2), '%Y-%m-%d')
    if type == 'day':
        day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (
                24 * 60 * 60)
    return abs(int(day_num))


if __name__ == "__main__":
    string = '25mg*20片'.lower()
    substring = '25mg*20片/瓶'.lower()
    out = KMP_algorithm(string, substring)
    print(out)
    a = '0.25g*100s'.lower()
    b = '0.25g*100T'.lower()
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
    jlist = jieba.cut(string,cut_all=True)
    for vax in jlist:
        print(vax)

    now1 = now()
    sdate  = datetime.datetime.strptime('2020.09.22','%Y.%m.%d')
    delta7 = datetime.timedelta(days=7)
    edate  = sdate + delta7
    print(edate)
    s = '2020-10-20 00:00:00'
    # print(now())
    if s < now():
        print('已过期,无法正常使用')
    else:
        print('未过期,可以正常使用')
    print(time_long('2020-09-22','2020-09-29'))
    now = datetime.date.today()
    print(now + relativedelta(months = 1))
    print(now + relativedelta(years = 1))
    print(now + relativedelta(days = 20))
