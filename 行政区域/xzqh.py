import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows',5000)

xzqh_html = requests.get('http://www.mca.gov.cn/article/sj/xzqh/2019/2019/201912251506.html')
print("xzqh_html_status_code: " + str(xzqh_html.status_code))
soup = BeautifulSoup(xzqh_html.text, 'html.parser')

xzqh_codes = []
xzqh_names = []

for sp in soup.find_all(attrs={"class" : "xl7028029"}):
    ts = sp.getText().strip()
    if ts.isdigit():
        xzqh_codes.append(ts)
    else :
        xzqh_names.append(ts)

xzqh_code_names = [ [xzqh_code, xzqh_name] for xzqh_code, xzqh_name in zip(xzqh_codes, xzqh_names) ]

xzqh_code_names_df = pd.DataFrame(xzqh_code_names, columns=['xzqh_code','xzqh_name'])
xzqh_code_names_df['xzqh_name'] = xzqh_code_names_df.xzqh_name.apply(lambda xzqh_name : '中国台湾省' if '台湾省' in xzqh_name else xzqh_name)
xzqh_code_names_df.head(3)

# 省份-直辖市-自治区-特别行政区处理
sf_zxs_zzq_tbxzqs = xzqh_code_names_df[xzqh_code_names_df.xzqh_code.str.endswith('0000')]
sf_zxs_zzq_tbxzqs['xzqh_ssq_code'] = sf_zxs_zzq_tbxzqs.xzqh_code.apply(lambda xzqh_code : xzqh_code[0:2])

xss = xzqh_code_names_df[(~xzqh_code_names_df.xzqh_code.str.endswith('0000')) & xzqh_code_names_df.xzqh_code.str.endswith('00')]
xss['xzqh_ssq_code'] = xss.xzqh_code.apply(lambda xzqh_code : xzqh_code[0:2])

# 省-下属市结果合并
union_df = pd.merge(sf_zxs_zzq_tbxzqs, xss, on='xzqh_ssq_code', how='left')
union_df.columns = ["province_code","province_name","xzqh_ssq_code","city_code","city_name"]

# 删除无效列
union_df = union_df.drop(columns='xzqh_ssq_code')

"""
空值列数据补充
"""
from numpy import NaN
def makeup_val(province_code,city_code):
    if city_code is NaN:
        return province_code
    else:
        return city_code
# 补充直辖市-特别行政区等空数据
union_df['city_code'] = union_df.apply(lambda rw: makeup_val(rw['province_code'],rw['city_code']),axis=1)
union_df['city_name'] = union_df.apply(lambda rw: makeup_val(rw['province_name'],rw['city_name']),axis=1)

# 格式化结果数据
union_df['province_code'] = union_df.province_code.apply(lambda province_code : province_code[0:2])
union_df['city_code'] = union_df.city_code.apply(lambda city_code : city_code[0:4])

# 导出结果性文件
union_df.to_csv("./2019年11月中华人民共和国县以上行政区划代码_省市_编码_中文名_340.csv",encoding='utf8',sep=',');
print(len(union_df.province_code.unique()), union_df.shape)