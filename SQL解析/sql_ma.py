import sql_metadata

sql = 'select * from aTable a join bTable b on a.id = b.id   where a.x = 1'
sql = ' '.join(sql.split())

if __name__ == '__main__':
    # 获取用到的全部的表
    print(sql_metadata.get_query_tables(sql))
    # 得到所有用到别名的表名与对应的别名
    print(sql_metadata.get_query_table_aliases(sql))