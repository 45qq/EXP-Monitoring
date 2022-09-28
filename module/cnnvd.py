import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                  "Chrome/98.0.4758.102 Safari/537.36"
}


def get_detail_old(url):
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=(5, 10), verify=False)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                detail_xq = soup.find(attrs={'class': 'detail_xq'})
                name = detail_xq.h2.string.strip()
                ul = detail_xq.ul.findAll('li')
                cnnvd_id = ul[0].span.string.replace('CNNVD编号：', '')
                cve_id = ul[2].a.string.strip()
                hazard_rating = ul[1].a.next.strip()
                cve_type = ul[3].a.string.strip()
                add_time = ul[4].a.string.strip()
                desc = ''
                for i in soup.find(attrs={'class': 'd_ldjj'}).findAll('p'):
                    p = i.string
                    if p:
                        desc += p.strip()
                return name, cnnvd_id, cve_id, desc, hazard_rating, cve_type, add_time
            else:
                print('cnnvd 获取信息出错！')
        except Exception as e:
            print('网络出错了！')
            print(e)
    print('cnnvd 获取信息失败！')
    print(url)


def get_cnnvd_detail_old(cnnvd):
    return get_detail_old('http://123.124.177.30/web/xxk/ldxqById.tag?CNNVD=%s' % cnnvd)


def get_detail_from_cve_old(cve):
    api = 'http://123.124.177.30/web/vulnerability/queryLds.tag?qcvCnnvdid=%s' % cve
    for i in range(3):
        try:
            res = requests.get(api, headers=headers, timeout=(5, 10), verify=False)
            if res.status_code == 200:
                tag = BeautifulSoup(res.text, 'html.parser').find(id='vulner_0')
                if not tag:
                    return
                url = 'http://123.124.177.30' + tag.find('a').get('href')
                detail = get_detail_old(url)
                if detail[2] == cve:
                    return detail
                return
            else:
                print('cnnvd 获取信息出错！')
        except Exception as e:
            print('网络出错了！')
            print(e)
    print('cnnvd 获取信息失败！')
    print(api)


def get_detail_from_cve(cve):
    return get_detail_from_cve_old(cve)


if __name__ == '__main__':
    # print(get_detail_from_cve_old('CVE-2022-3296'))
    # print(get_detail('https://www.cnnvd.org.cn/home/globalSearch?keyword=CVE-2022-30781'))
    pass