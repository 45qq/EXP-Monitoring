import re
import time
import requests
import urllib3
import db.mydb as mydb
from datetime import datetime
from lib.config import github_monitor_config
from module.cvemitre import get_cve_detail
from module.cnnvd import get_detail_from_cve

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                  "Chrome/98.0.4758.102 Safari/537.36"
}

github_headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "token {}".format(github_monitor_config['token'])
}

urllib3.disable_warnings()

github_update_key: list = github_monitor_config['update_key']
enable_exact_match: bool = github_monitor_config['enable_exact_match']
lowest_star: int = github_monitor_config['push_config']['lowest_star']
growth_warning_star: list = github_monitor_config['push_config']['growth_warning_star']
name_warning_count: list = github_monitor_config['push_config']['name_warning_count']

year = datetime.now().year
for index in range(len(github_update_key)):
    github_update_key[index] = github_update_key[index].format(year=year, year_1=year - 1, year_2=year - 2,
                                                               year_3=year - 3, year_4=year - 4, year_5=year - 5,
                                                               year_6=year - 6, year_7=year - 7, year_8=year - 8,
                                                               year_9=year - 9, year_10=year - 10)
growth_warning_star.sort(reverse=True)
name_warning_count.sort(reverse=True)


def get_res(url):
    try:
        time.sleep(1)
        res = requests.get(url, headers=github_headers, timeout=(5, 10), verify=False)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            print('无效的 token 凭据！')
            return
        elif res.status_code == 403:
            print('超过登录失败的最大次数。请稍后再试。')
            return
    except Exception as e:
        print('网络出错了！')
        print(e)


def get_json(url):
    for i in range(3):
        json_str = get_res(url)
        if json_str:
            return json_str


def get_q(key):
    if enable_exact_match:
        return 'in:name %s' % key
    else:
        return key


def get_name_key(name, desc, key):
    if re.search(r'cve-\d\d\d\d', key, re.I):
        re_name = re.search(r'cve-\d\d\d\d-\d{4,5}', '%s %s' % (name, desc), re.I)
        if re_name:
            return re_name.group().upper()
        return -1


def is_match(name, desc, key):
    key = re.sub(r'[-_ ]', '.?', key)
    if re.search(r'\b%s\b' % key, '%s %s' % (name, desc), re.I):
        return True
    return False


def init():
    print('开始 github 数据库初始化: ')
    init_data_sum = 0
    for key in github_update_key:
        api = 'https://api.github.com/search/repositories?q="{}"&sort=updated&per_page=30'.format(get_q(key))
        json_str = get_json(api)
        if not json_str:
            print('[-] %s 查询失败！' % key)
            continue

        items: list = json_str['items']
        rows = []
        for i in items:
            name = i['name']
            description = i['description']
            if not is_match(name, description, key):
                continue
            full_name = i['full_name']
            star = i['stargazers_count']
            name_key = get_name_key(name, description, key)
            if name_key == -1:
                continue
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            rows.append((name, description, star, name_key, full_name, dt))

        rows = mydb.insert_github_info(rows)
        init_data_sum += len(rows)
        print('[*] %s 增加 %d 条' % (key, len(rows)))
    print('github 数据库初始化完成！增加 %d 条。\n' % init_data_sum)


def update():
    print('来自 github 更新: ')
    for key in github_update_key:
        api = 'https://api.github.com/search/repositories?q="{}"&sort=updated'.format(get_q(key))
        json_str = get_json(api)
        if not json_str:
            print('[-] %s 查询失败！' % key)
            continue

        items: list = json_str['items']
        rows = []
        for i in items:
            name = i['name']
            description = i['description']
            if not is_match(name, description, key):
                continue
            full_name = i['full_name']
            star = i['stargazers_count']
            name_key = get_name_key(name, description, key)
            if name_key == -1:
                continue
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            rows.append((name, description, star, name_key, full_name, dt))

        rows = mydb.insert_github_info(rows)
        rows = mydb.insert_github_info_push(rows, lowest_star)
        print('[*] %s 增加 %d 条' % (key, len(rows)))
        for row in rows:
            name = row[0]
            description = row[1]
            full_name = row[4]
            star = row[2]
            print('[+]\tname: %s\n\tdescription: %s\n\tfull_name: %s\n\tstar: %s\n' % (
                name, description, full_name, star))
    print('\n')


def is_arrive(num, num_list):
    for i in num_list:
        if num > i:
            return i


def monitor():
    print('来自 github 监控: ')
    # 监控项目星
    items = mydb.select_github_monitor_list_view()
    rows = []
    for info_id, full_name, star, add_time_today in items:
        api = "https://api.github.com/repos/{}".format(full_name)
        json_str = get_json(api)
        if not json_str:
            print('[-] %s 查询失败！' % full_name)
            continue

        latest_star = json_str['stargazers_count']
        if latest_star != star:
            growth_star = latest_star - star
            rows.append((info_id, latest_star, time.localtime(time.time())))
            print('[*] %s %d星 增长了%d星' % (full_name, latest_star, growth_star))
    mydb.insert_github_star(rows)

    # 星变化达到推送要求的加入推送列表
    items = mydb.select_github_star()
    rows = []
    for item in items:
        change_star = item[2]
        for i in growth_warning_star:
            if change_star >= i:
                rows.append((item[0], change_star, 0))
                break
    rows = mydb.insert_github_star_push(rows)
    for i in rows:
        full_name = i[0]
        change_star = i[1]
        print('[+] %s 增长了%d星' % (full_name, change_star))

    # cve 仓库数量计数达到推送要求的加入推送列表
    items = mydb.select_github_name_key()
    rows = []
    for item in items:
        count = item[1]
        for i in name_warning_count:
            if count >= i:
                rows.append((item[0], item[1], 0))
                break
    rows = mydb.insert_github_name_key_push(rows)
    for i in rows:
        name = i[0]
        count = i[1]
        print('[+] %s 仓库数量达到%d个' % (name, count))

    print('\n')


def run():
    update()
    monitor()


def other_desc(cve: str, show_cve):
    if not cve or cve.isspace():
        return ''
    detail = get_detail_from_cve(cve)
    if detail:
        return '> CNNVD %s信息  \n危害：%s  \n类型：%s  \n简介：%s  \n\n' % \
               (cve + ' ' if show_cve else '', detail[4], detail[5], detail[3])
    detail = get_cve_detail(cve)
    if detail:
        return '> CVE-MITRE 描述：%s  \n\n' % detail[1]
    return ''


def get_push_md():
    rows1 = mydb.select_github_info_push()
    rows2 = mydb.select_github_star_push()
    rows3 = mydb.select_github_name_key_push()
    l1 = len(rows1)
    l2 = len(rows2)
    l3 = len(rows3)
    if not (l1 or l2 or l3):
        return
    brief_msg = 'github 更新了 %d/%d/%d 条内容！' % (l1, l2, l3)
    detailed_msg = '##### 更新时间：%s  \n' % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if l1:
        detailed_msg += '☆ github 更新了 %d 条内容！  \n' % l1
    if l2:
        detailed_msg += '☆ github 星监控有 %d 条新发现！  \n' % l2
    if l3:
        detailed_msg += '☆ github 仓库数量监控有 %d 条新发现！  \n\n' % l3
    if l1:
        detailed_msg += '## Github 更新内容(%d)  \n---' % l1
        for i in range(l1):
            row = rows1[i]
            detailed_msg += """
### %d. %s [∞](%s)  
标星：%s  
关于：%s  
%s  
```
%s
```  
""" % (i + 1, row[0], row[3], row[2], row[1], other_desc(row[4], True), row[3])
    if l2:
        detailed_msg += '## Github 标星监控发现(%d)  \n---' % l2
        for i in range(l2):
            row = rows2[i]
            detailed_msg += """
### %d. %s [∞](%s)  
标星：%s  **↑%s**  
关于：%s  
%s  
```
%s
```
""" % (i + 1, row[0], row[4], row[2], row[3], row[1], other_desc(row[5], True), row[4])
    if l3:
        detailed_msg += '## Github 仓库数量监控发现(%d)  \n---' % l3
        for i in range(l3):
            row = rows3[i]
            detailed_msg += """
### %d. 关键词：%s  
%s仓库数：%s  
总标星：%s  
相关链接：  
```
%s
```
""" % (i + 1, row[0], other_desc(row[0], False), row[1], row[2], '  \n'.join(row[3].split(',')))
    print(brief_msg)
    print(detailed_msg)
    return brief_msg, detailed_msg


def finish_push():
    mydb.finish_github_push()


if __name__ == '__main__':
    init()
    # update()
    # monitor()
    import lib.push as p
    p.send()
