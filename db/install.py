import pymysql
import sys
import os
from lib.config import root_dir
from db.mydb import host, port, user, password, db


def read_sql_file(filename, encoding):
    with open(filename, 'r', encoding=encoding) as f:
        data = f.readlines()
        stmts = []
        delimiter = ';'
        stmt = ''

        for lineno, line in enumerate(data):
            if not line.strip():
                continue

            if line.startswith('--'):
                continue

            if 'DELIMITER' in line:
                delimiter = line.split()[1]
                continue

            if delimiter not in line:
                stmt += line.replace(delimiter, ';')
                continue

            if stmt:
                stmt += line
                stmts.append(stmt.strip())
                stmt = ''
            else:
                stmts.append(line.strip())
        return stmts


def parse_sql(filename):
    for i in ['gbk', 'utf-8', 'utf-16']:
        return read_sql_file(filename, i)


def execute_sql_file(filename, cursor):
    for command in parse_sql(filename):
        try:
            cursor.execute(command)
        except Exception as msg:
            print("错误信息： ", msg)

    print('sql 执行完成')


def get_conn():
    try:
        conn = pymysql.connect(host=host, user=user, password=password, port=port, charset='utf8',
                               sql_mode='STRICT_ALL_TABLES,STRICT_TRANS_TABLES')
        if not conn:
            print('数据库连接失败了！')
            sys.exit()
        return conn
    except Exception as e:
        print('数据库连接失败了！')
        print(e)
        sys.exit()


def install():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute('show databases like %s', db)
            sql_file = os.path.join(os.path.join(root_dir, 'db'), 'exp-monitoring.sql')
            if not cursor.fetchone():
                print('开始安装数据库！')
                cursor.execute('create database `%s`' % db)
                conn.select_db(db)
                execute_sql_file(sql_file, cursor)
                conn.commit()
                print('数据库安装完成。')
                return True
            else:
                conn.select_db(db)
                cursor.execute('show tables')
                if not cursor.fetchone():
                    print('开始安装数据库！')
                    execute_sql_file(sql_file, cursor)
                    conn.commit()
                    print('数据库安装完成。')
                    return True
                else:
                    print('数据库已安装。')


if __name__ == '__main__':
    install()