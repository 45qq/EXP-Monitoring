import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from lib.config import push_config
from module.github_monitor import get_push_md, finish_push
from lib.md_tran import md_to_html
from dingtalkchatbot.chatbot import DingtalkChatbot


def server_chan_send(title: str, content: str):
    params = {
        "text": title,
        "desp": content,
    }
    send_key = push_config['server_chan']['send_key']
    send_api = "https://sctapi.ftqq.com/%s.send" % send_key

    for i in range(3):
        try:
            res = requests.post(send_api, data=params, timeout=(5, 10), verify=False)
            if res.status_code == 200 and res.text.find("SUCCESS") != -1:
                print("[+] Server酱推送成功。")
                return True
            else:
                print('[-] Server酱推送失败！')
                print(res.text)
        except Exception as e:
            print('网络出错了！')
            print(e)
    return False


def email(title: str, content: str):
    mail = push_config['email']
    smtp_server = mail['smtp_server']
    smtp_port = mail['smtp_port']
    from_addr = mail['from_addr']
    password = mail['password']
    to_addr = mail['to_addr']

    msg = MIMEText(md_to_html(content), 'html', 'utf-8')
    msg['From'] = Header('EXP-Monitoring')
    msg['Subject'] = Header(title, 'utf-8')

    smtp_obj = None
    for i in range(3):
        try:
            smtp_obj = smtplib.SMTP_SSL(smtp_server)
            smtp_obj.connect(smtp_server, smtp_port)
            smtp_obj.login(from_addr, password)
            smtp_obj.sendmail(from_addr, to_addr, msg.as_string())
            print("[+] 邮件发送成功。")
            return True
        except smtplib.SMTPException:
            print("[-] 发送邮件失败！")
        finally:
            smtp_obj.quit()
    return False


def dingding(title: str, content: str):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % push_config['dingding']['access_token']
    for i in range(3):
        try:
            bot = DingtalkChatbot(webhook, secret=push_config['dingding']['secret'])
            result = bot.send_markdown(title=title, text=content)
            if result.get('errcode'):
                print('[-] 钉钉推送失败！')
                print(result)
            else:
                print("[+] 钉钉推送成功。")
                return True
        except Exception as e:
            print('[-] 钉钉推送失败！')
            print(e)
    return False


def base_send(title: str, content: str):
    if push_config['server_chan']['enable'] and server_chan_send(title, content):
        finish_push()
    if push_config['email']['enable'] and email(title, content):
        finish_push()
    if push_config['dingding']['enable'] and dingding(title, content):
        finish_push()


def send():
    github_push = get_push_md()
    if github_push:
        base_send(github_push[0], github_push[1])


if __name__ == '__main__':
    md = get_push_md()
    dingding('123', '456')
