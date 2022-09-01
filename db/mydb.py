import sys

import pymysql


class Mydp:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '@123456z'
        self.db = 'exp-monitoring'
        self.conn = None

    def get_cur(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                        db=self.db, port=self.port, charset='utf8')
        except Exception:
            print('数据库连接失败了！')
            sys.exit()

        cur = self.conn.cursor()
        if not cur:
            print('数据库连接失败了！')
        return cur

    def insert(self, sql, rows):
        cur = self.get_cur()
        numerator = 0
        affected_rows = []
        for row in rows:
            cur.execute(sql, row)
            if self.conn.affected_rows().numerator:
                numerator += 1
                affected_rows.append(row)
        self.conn.commit()
        self.conn.close()
        return affected_rows

    def select(self, sql):
        cur = self.get_cur()
        cur.execute(sql)
        rows = cur.fetchall()
        self.conn.close()
        return rows

    def insert_github_info(self, rows):
        sql = 'insert ignore into github_info(name, description, star, name_key, full_name, add_time) values(%s, %s, %s, %s, %s, %s)'
        return self.insert(sql, rows)

    def insert_github_info_push(self, rows, lowest_star):
        sql = '''insert ignore into github_info_push_list(id, is_push)
                 values((select id from github_info where full_name=%s), 0)'''
        cur = self.get_cur()
        numerator = 0
        affected_rows = []
        for row in rows:
            if row[2] < lowest_star:
                continue
            full_name = row[4]
            cur.execute(sql, full_name)
            if self.conn.affected_rows().numerator:
                numerator += 1
                affected_rows.append(row)
        self.conn.commit()
        self.conn.close()
        return affected_rows

    def select_github_monitor_list_view(self):
        sql = 'select id, full_name, latest_star, update_time from github_monitor_list_view'
        return self.select(sql)

    def insert_github_star(self, rows):
        sql = 'insert into github_star_list(id, star, update_time) ' \
              'values(%s, %s, %s) on duplicate key update star=%s'
        cur = self.get_cur()
        numerator = 0
        affected_rows = []
        for row in rows:
            cur.execute(sql, (row[0], row[1], row[2], row[1]))
            if self.conn.affected_rows().numerator:
                numerator += 1
                affected_rows.append(row)
        self.conn.commit()
        self.conn.close()
        return affected_rows

    def select_github_star(self):
        sql = '''select gscv.id, full_name, latest_star - gscv.init_star
                 from github_info join github_star_change_view gscv on github_info.id = gscv.id'''
        return self.select(sql)

    def insert_github_star_push(self, rows):
        sql1 = 'insert ignore into github_star_change_push_list(id, growth_star, push_grade) values(%s, %s, %s)'
        sql2 = 'update github_star_change_push_list set growth_star=%s where id=%s and growth_star < %s'
        cur = self.get_cur()
        numerator = 0
        affected_rows = []
        for row in rows:
            cur.execute(sql1, (row[0], row[2]))
            if self.conn.affected_rows().numerator:
                numerator += 1
                affected_rows.append(row)
            else:
                cur.execute(sql2, (row[2], row[0], row[2]))
                if self.conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)

        self.conn.commit()
        self.conn.close()
        return affected_rows

    def select_github_name_key(self):
        sql = 'select name_key, count from github_name_key_list_view'
        return self.select(sql)

    def insert_github_name_key_push(self, rows):
        sql1 = 'insert ignore into github_name_key_push_list(name_key, count, push_grade) values(%s, %s, %s)'
        sql2 = 'update github_name_key_push_list set count=%s where name_key=%s and count < %s'
        cur = self.get_cur()
        numerator = 0
        affected_rows = []
        for row in rows:
            cur.execute(sql1, row)
            if self.conn.affected_rows().numerator:
                numerator += 1
                affected_rows.append(row)
            else:
                cur.execute(sql2, (row[1], row[0], row[1]))
                if self.conn.affected_rows().numerator:
                    numerator += 1
                    affected_rows.append(row)

        self.conn.commit()
        self.conn.close()
        return affected_rows

    def select_github_info_push(self):
        sql = 'select name, description, star, concat("https://github.com/", full_name) ' \
              'from github_info join github_info_push_list gipl on github_info.id = gipl.id ' \
              'where is_push=0 order by star desc'
        return self.select(sql)

    def select_github_star_push(self):
        sql = 'select name, description, star, growth_star, concat("https://github.com/", full_name) ' \
              'from github_info join github_star_change_push_list gscpl ' \
              'on github_info.id = gscpl.id where growth_star > gscpl.push_grade order by growth_star desc, star desc'
        return self.select(sql)

    def select_github_name_key_push(self):
        sql = 'select gnpl.name_key, gnpl.count, sum(star) as s, ' \
              'group_concat(concat("https://github.com/", full_name)) ' \
              'from github_info join github_name_key_push_list gnpl on github_info.name_key = gnpl.name_key ' \
              'join github_name_key_list gnkl on gnkl.name_key = gnpl.name_key ' \
              'where gnpl.count > push_grade group by gnpl.name_key  order by gnpl.count desc, s desc'
        return self.select(sql)

    def finish_github_push(self):
        sql1 = 'update github_info_push_list set is_push=1 where is_push = 0'
        sql2 = 'update github_star_change_push_list set push_grade=growth_star where push_grade < growth_star'
        sql3 = 'update github_name_key_push_list set push_grade=count where push_grade < count'
        cur = self.get_cur()
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        self.conn.commit()
        self.conn.close()


mydb = Mydp()

if __name__ == '__main__':
    # mydb.insert_github([('2022-LPE-UAF', '1', 0, '5', '2022-08-27 13:49:13')])
    print(mydb.insert_github_star_change_push([(165126, 0, 0)]))
