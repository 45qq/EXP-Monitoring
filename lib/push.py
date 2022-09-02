import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from lib.config import push_config
from module.github_monitor import get_push, finish_push
from lib.md_to_html import md2html


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

    msg = MIMEText(md2html(content), 'html', 'utf-8')
    msg['From'] = Header('EXP-Monitoring')
    msg['Subject'] = Header(title, 'utf-8')

    smtpobj = None
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        smtpobj.connect(smtp_server, smtp_port)
        smtpobj.login(from_addr, password)
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("[+] 邮件发送成功。")
        return True
    except smtplib.SMTPException:
        print("[-] 发送邮件失败！")
    finally:
        smtpobj.quit()
    return False


def send():
    github_push = get_push()
    if push_config['server_chan']['enable'] and server_chan_send(github_push[0], github_push[1]):
        finish_push()
    if push_config['email']['enable'] and email(github_push[0], github_push[1]):
        finish_push()


if __name__ == '__main__':
    pass