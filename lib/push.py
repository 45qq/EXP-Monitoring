import requests
from module.github_monitor import get_push, finish_push


def get_res(url, params):
    try:
        res = requests.post(url, data=params, timeout=(5, 10), verify=False)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print('网络出错了！')
        print(e)


def get_json(url, params):
    for i in range(3):
        json_str = get_res(url, params)
        if json_str:
            return json_str


def server_chan_send(title: str, content: str):
    params = {
        "text": title,
        "desp": content,
    }
    send_key = ''
    send_api = "https://sctapi.ftqq.com/%s.send" % send_key

    for i in range(3):
        try:
            res = requests.post(send_api, data=params, timeout=(5, 10), verify=False)
            if res.status_code == 200 and res.text.find("SUCCESS") != -1:
                print("推送成功。")
                return True
            else:
                print('[-] 推送失败！')
                print(res.text)
        except Exception as e:
            print('网络出错了！')
            print(e)
    return False


def send():
    github_push = get_push()
    if server_chan_send(github_push[0], github_push[1]):
        finish_push()


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                      "Chrome/98.0.4758.102 Safari/537.36"
    }
    res = requests.get('https://raw.githubusercontent.com/jenkins-docs/building-a-multibranch-pipeline-project/master/README.md', headers=headers)
    print(res.text)