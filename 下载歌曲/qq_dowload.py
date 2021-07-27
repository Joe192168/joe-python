import requests

headers={
    'accept': '*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'kg_mid=ebb2de813317a791bcf7b7d3131880c4; UM_distinctid=1722ba8b22632d-07ac0227c507a7-4e4c0f20-1fa400-1722ba8b2284a1; kg_dfid=0Q0BEI47P4zf0mHYzV0SYbou; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1590041687,1590280210,1590367138,1590367386; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1590367431',
    'referer': 'https://www.kugou.com/yy/html/search.html',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
aa=input('请输入歌名：')
data={
    'callback': 'jQuery112408716317197794392_1590368232677',
    'keyword':aa,
    'page': '1',
    'pagesize':'30',
    'userid':'-1',
    'clientver': '',
    'platform': 'WebFilter',
    'tag': 'em',
    'filter': '2',
    'iscorrection': '1',
    'privilege_filter': '0',
    '_': '1590368232679',
}
res = requests.get('https://www.kugou.com/yy/html/search.html',params=data,timeout=4)
print(res)