import sys
import pymysql
import cryptography
from lib.config import mysql_config, github_monitor_config


host = mysql_config['host']
port = mysql_config['port']
user = mysql_config['user']
password = mysql_config['password']
db = mysql_config['db']


def get_conn():
    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset='utf8',
                               sql_mode='STRICT_ALL_TABLES,STRICT_TRANS_TABLES')
        if not conn:
            print('数据库连接失败了！')
            sys.exit()
        return conn
    except Exception as e:
        print('数据库连接失败了！')
        print(e)
        sys.exit()


def insert(sql, rows):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            numerator = 0
            affected_rows = []
            for row in rows:
                cursor.execute(sql, row)
                if conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)
            conn.commit()
            return affected_rows


def select(sql, args=None):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, args)
            rows = cursor.fetchall()
    return rows


def insert_github_info(rows):
    sql = 'insert ignore into github_info(name, description, star, name_key, full_name, add_time)' \
          ' values(%s, %s, %s, %s, %s, %s)'
    return insert(sql, rows)


def insert_github_info_push(rows, lowest_star):
    sql = '''insert ignore into github_info_push_list(id, is_push)
             values((select id from github_info where full_name=%s), 0)'''
    with get_conn() as conn:
        with conn.cursor() as cursor:
            numerator = 0
            affected_rows = []
            for row in rows:
                if row[2] < lowest_star:
                    continue
                full_name = row[4]
                cursor.execute(sql, full_name)
                if conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)
            conn.commit()
            return affected_rows


def select_github_monitor_list_view():
    sql = 'select id, full_name, latest_star from  github_star_change_view ' \
          'where add_time_today <= %s limit %s'
    return select(sql, (github_monitor_config['monitoring']['duration'],
                        github_monitor_config['monitoring']['max_number']))


def insert_github_star(rows):
    sql = 'insert into github_star_list(id, star, update_time) ' \
          'values(%s, %s, %s) on duplicate key update star=%s'
    with get_conn() as conn:
        with conn.cursor() as cursor:
            numerator = 0
            affected_rows = []
            for row in rows:
                cursor.execute(sql, (row[0], row[1], row[2], row[1]))
                if conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)
            conn.commit()
            return affected_rows


def select_github_star():
    sql = 'select id, full_name, latest_star - init_star from github_star_change_view ' \
          'where add_time_today <= %s order by (latest_star - init_star) desc'
    return select(sql, github_monitor_config['monitoring']['duration'])


def insert_github_star_push(rows):
    sql1 = 'insert ignore into github_star_change_push_list(id, growth_star, push_grade) values(%s, %s, %s)'
    sql2 = 'update github_star_change_push_list set growth_star=%s where id=%s and growth_star < %s'
    with get_conn() as conn:
        with conn.cursor() as cursor:
            numerator = 0
            affected_rows = []
            for row in rows:
                cursor.execute(sql1, row)
                if conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)
                else:
                    cursor.execute(sql2, (row[2], row[0], row[2]))
                    if conn.affected_rows().numerator:
                        numerator += 1
                        affected_rows.append(row)

            conn.commit()
            return affected_rows


def select_github_name_key():
    sql = 'select name_key, count from github_name_key_list_view where update_time_today <= %s'
    return select(sql, github_monitor_config['monitoring']['duration'])


def insert_github_name_key_push(rows):
    sql1 = 'insert ignore into github_name_key_push_list(name_key, count, push_grade) values(%s, %s, %s)'
    sql2 = 'update github_name_key_push_list set count=%s where name_key=%s and count < %s'
    with get_conn() as conn:
        with conn.cursor() as cursor:
            numerator = 0
            affected_rows = []
            for row in rows:
                cursor.execute(sql1, row)
                if conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)
                else:
                    cursor.execute(sql2, (row[1], row[0], row[1]))
                    if conn.affected_rows().numerator:
                        numerator += 1
                        affected_rows.append(row)

            conn.commit()
            return affected_rows


def select_github_info_push():
    sql = 'select name, description, star, concat("https://github.com/", full_name), name_key ' \
          'from github_info join github_info_push_list gipl on github_info.id = gipl.id ' \
          'where is_push=0 order by star desc'
    return select(sql)


def select_github_star_push():
    sql = 'select name, description, star + growth_star, growth_star, concat("https://github.com/", full_name), ' \
          'name_key from github_info join github_star_change_push_list gscpl on github_info.id = gscpl.id ' \
          'where growth_star > gscpl.push_grade order by growth_star desc, (star + growth_star) desc'
    return select(sql)


def select_github_name_key_push():
    sql = 'select gscv.name_key, count, sum(latest_star) as l, ' \
          'group_concat(concat("https://github.com/", full_name, "\t标星：", latest_star)) ' \
          'from github_name_key_push_list gnkpl join github_star_change_view gscv on gnkpl.name_key = gscv.name_key ' \
          'where gnkpl.count > gnkpl.push_grade group by gscv.name_key order by count desc, l desc'
    return select(sql)


def finish_github_push():
    sql1 = 'update github_info_push_list set is_push=1 where is_push = 0'
    sql2 = 'update github_star_change_push_list set push_grade=growth_star where push_grade < growth_star'
    sql3 = 'update github_name_key_push_list set push_grade=count where push_grade < count'
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
        conn.commit()


if __name__ == '__main__':
    with get_conn().cursor() as cur:
        cur.execute('select 1')
        print(cur.fetchall())
