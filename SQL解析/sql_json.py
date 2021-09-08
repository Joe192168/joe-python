from moz_sql_parser import parse
import re
import json

sql = 'select * from aTable a join bTable b on a.id = b.id   where a.x = 1'

def clean_comment(sql):
    # 删除多行注释
    sql = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql)
    # 删除独立一行注释
    lines = [line for line in sql.splitlines() if not re.match("^\s*(--|#)", line)]
    # 删除代码末尾行注释
    sql = " ".join([sql.split("--|#", line)[0] for line in lines])
    sql = ' '.join(sql.split())
    return sql

def get_all_tales(sql):
    #找到所有涉及到的表名
    sql_tree = parse(sql)
    print(json.dumps(sql_tree))
    from_t = sql_tree['from']
    all_tables = []
    alias_tables = {}
    if isinstance(from_t,list):
        #join结构
        print(f'join结构{from_t}')
        for join_r in from_t:
            if 'join' in join_r:
                if isinstance(join_r["join"],dict):
                    print(f'join表名:{join_r["join"]["value"]},别名:{join_r["join"]["name"]}')
                    all_tables.append(join_r["join"]["value"])
                    alias_tables.update({join_r["join"]["value"]: join_r["join"]["name"]})
                else:
                    print(f'join表名:{join_r["join"]}')
                    all_tables.append(join_r["join"])
            elif 'left join' in join_r:
                if isinstance(join_r["left join"],dict):
                    print(f'left join表名:{join_r["left join"]["value"]},别名:{join_r["left join"]["name"]}')
                    all_tables.append(join_r["left join"]["value"])
                    alias_tables.update({join_r["left join"]["value"]: join_r["left join"]["name"]})
                else:
                    print(f'left join表名:{join_r["left join"]}')
                    all_tables.append(join_r["left join"])
            elif 'right join' in join_r:
                if isinstance(join_r["right join"],dict):
                    print(f'right join表名:{join_r["right join"]["value"]},别名:{join_r["right join"]["name"]}')
                    all_tables.append(join_r["right join"]["value"])
                    alias_tables.update({join_r["right join"]["value"]: join_r["right join"]["name"]})
                else:
                    print(f'right join表名:{join_r["right join"]}')
                    all_tables.append(join_r["right join"])
            elif 'inner join' in join_r:
                if isinstance(join_r["inner join"],dict):
                    print(f'inner join表名:{join_r["inner join"]["value"]},别名:{join_r["inner join"]["name"]}')
                    all_tables.append(join_r["inner join"]["value"])
                    alias_tables.update({join_r["inner join"]["value"]: join_r["inner join"]["name"]})
                else:
                    print(f'inner join表名:{join_r["inner join"]}')
                    all_tables.append(join_r["inner join"])
            elif 'full join' in join_r:
                if isinstance(join_r["full join"],dict):
                    print(f'full join表名:{join_r["full join"]["value"]},别名:{join_r["full join"]["name"]}')
                    all_tables.append(join_r["full join"]["value"])
                    alias_tables.update({join_r["full join"]["value"]: join_r["full join"]["name"]})
                else:
                    print(f'full join表名:{join_r["full join"]}')
                    all_tables.append(join_r["full join"])
            elif 'left outer join' in join_r:
                if isinstance(join_r["left outer join"],dict):
                    print(f'left outer join表名:{join_r["left outer join"]["value"]},别名:{join_r["left outer join"]["name"]}')
                    all_tables.append(join_r["left outer join"]["value"])
                    alias_tables.update({join_r["left outer join"]["value"]: join_r["left outer join"]["name"]})
                else:
                    print(f'left outer join表名:{join_r["left outer join"]}')
                    all_tables.append(join_r["left outer join"])
            elif 'right outer join' in join_r:
                if isinstance(join_r["right outer join"],dict):
                    print(f'right outer join表名:{join_r["right outer join"]["value"]},别名:{join_r["right outer join"]["name"]}')
                    all_tables.append(join_r["right outer join"]["value"])
                    alias_tables.update({join_r["right outer join"]["value"]: join_r["right outer join"]["name"]})
                else:
                    print(f'right outer join表名:{join_r["right outer join"]}')
                    all_tables.append(join_r["right outer join"])
            elif 'full outer join' in join_r:
                # right join
                if isinstance(join_r["full outer join"],dict):
                    print(f'full outer join表名:{join_r["full outer join"]["value"]},别名:{join_r["full outer join"]["name"]}')
                    all_tables.append(join_r["full outer join"]["value"])
                    alias_tables.update({join_r["full outer join"]["value"]: join_r["full outer join"]["name"]})
                else:
                    print(f'full outer join表名:{join_r["full outer join"]}')
                    all_tables.append(join_r["full outer join"])
            else:
                print("")
    else:
        if isinstance(from_t, dict):
            print(f'全部的表:{from_t},别名{from_t[ "name" ]}')

if __name__ == '__main__':
    #tree = parse(sql)
    #print(json.dumps(tree))
    #sql = clean_comment(sql)
    get_all_tales(sql)
