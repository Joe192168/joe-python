import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                yield from extract_from_part(item)
            elif item.ttype is Keyword:
                return
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value


def extract_tables(sql):
    stream = extract_from_part(sqlparse.parse(sql)[0])
    return list(extract_table_identifiers(stream))


if __name__ == '__main__':
    sql = """
    select   Distinct b.office_name as 住院科室,   tcd1.cp_name as 路径,   Fpp.Leave_Hosp_Time as 日期,   Fpp.Inpatient_Id as 住院号,   aa.disease_name as 入院诊断,   tup.user_name as 主管医师,   cc.personal_name as 患者姓名,   tup.user_name as 主管医师,   toc.outcp_class as 状态,   fpp.in_cp_time as 入径时间,   fpp.ou_cp_time as 出径时间,   fpp.hospital_day as 住院天数,   tcv.stand_hospital_days as 标准住院天数,   ceil(TO_NUMBER(fpp.ou_cp_time - fpp.in_cp_time)) 入径天数,   (     select       sum(ficr.total_money) as money     from       f_medical_record_homepage ficr     where       ficr.leave_hosp_time >= fpp.in_cp_time       and ficr.leave_hosp_time <= fpp.ou_cp_time       and ficr.inpatient_id = fpp.inpatient_id   ) as 入径花费,   (     select       sum(ficr1.total_money) as money     from       f_medical_record_homepage ficr1     where       ficr1.inpatient_id = fpp.inpatient_id   ) as 费用合计 From   (     select       *     from       (         select           row_number() over(             partition by fpp.inpatient_id,             Fpp.BEHOSP_OFFICE             order by               fpp.in_cp_time desc           ) rn,           fpp.cp_id,           fpp.inpatient_id,           Fpp.Inhos_Diagnose_Id,           Fpp.BEHOSP_OFFICE,           Fpp.Inhosp_Time,           fpp.leave_hosp_time,           fpp.behosp_doctor,           outcp_class_id,           ou_cp_time,           hospital_day,           fpp.in_cp_time         from           f_Patient_Path Fpp       )     where       rn = 1   ) fpp   inner Join t_Cp_Disease Tcd On Fpp.Inhos_Diagnose_Id = Tcd.Disease_Id   And Fpp.Cp_Id = Tcd.Cp_Id   inner join t_Disease_Directory aa on aa.id = tcd.disease_id   inner join f_inpatient_record bb on fpp.inpatient_id = bb.id   inner join f_personal_info cc on bb.patient_id = cc.id   inner JOIN T_OFFICE_PROPERTY B ON Fpp.BEHOSP_OFFICE = B.ID   and b.is_reject = 0   left join t_cp_dictionary tcd1 on fpp.cp_id = tcd1.id   left join t_user_property tup on tup.id = fpp.behosp_doctor   left join t_outcp_class toc on fpp.outcp_class_id = toc.id   left join T_CP_VERSION tcv on tcv.cp_id = fpp.cp_id group by   Fpp.Leave_Hosp_Time ， Tcd.Disease_Id,   Fpp.Behosp_Office,   b.office_name,   b.hospital_dis,   Fpp.Inpatient_Id ， tcd1.cp_name,   aa.disease_name,   tup.user_name,   cc.personal_name ， toc.outcp_class,   fpp.in_cp_time,   fpp.ou_cp_time,   fpp.hospital_day,   tcv.stand_hospital_days
    """

    tables = ', '.join(extract_tables(sql))
    print('Tables: {}'.format(tables))