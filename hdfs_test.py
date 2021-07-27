# -*- coding: utf-8 -*-
import pandas as pd
import hdfs
_author_ = 'joe'
_date_ = '2021/07/22'


hdfs_user = 'root'
hdfs_addr = 'http://192.168.0.233:9870'
client = hdfs.InsecureClient(hdfs_addr, user=hdfs_user)
df = pd.read_csv("D:\\user_visit_action.csv")
print(df)
hdfs_path = '/test/a.csv'
client.write(hdfs_path, df.to_csv(index=False), overwrite=True, encoding='utf-8')
read = client.read(hdfs_path, encoding='utf-8')
with read as reader:
    for row in reader:
        print(row)