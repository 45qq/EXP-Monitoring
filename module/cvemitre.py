import requests
import urllib3
import re
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                  "Chrome/98.0.4758.102 Safari/537.36"
}


urllib3.disable_warnings()


def get_detail(url):
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=(5, 10), verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                cve_id = soup.find(nowrap='nowrap').find('h2').string
                table = soup.find(id='GeneratedTable').find('table')
                td = table.find_all('tr')[3].find('td')
                description = td.string
                if not description:
                    description = ''
                    for string in td.stripped_strings:
                        description += string
                company = table.find_all('tr')[8].find('td').string
                createdate = table.find_all('tr')[10].find('td').string
                description = re.sub(r'&#\d+;', '', str(description)).strip()
                return cve_id, description, company, createdate
            else:
                print('cve-mitre 获取信息出错！')
        except Exception as e:
            print('网络出错了！')
            print(e)
    print('cve-mitre 获取信息失败！')


def get_cve_detail(cve):
    return get_detail('https://cve.mitre.org/cgi-bin/cvename.cgi?name=%s' % cve)


if __name__ == '__main__':
    print(get_detail("https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-37176"))
