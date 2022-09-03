#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author: 四五qq
# source: https://github.com/45qq/EXP-Monitoring
import module.github_monitor as gm
from lib.push import send, base_send
from lib.config import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from db.install import install
from db.mydb import update_config


sched = BackgroundScheduler(timezone='Asia/Shanghai')


def init():
    if install():
        gm.init()
    update_config()
    gm.run()
    base_send('EXP-Monitoring 初始化完成！', 'EXP-Monitoring 初始化完成！')


if __name__ == '__main__':
    init()

    print('开始监控计划。')
    github_run_schedule = schedule['github_run']
    push_schedule = schedule['push']

    scheduler = BlockingScheduler()
    scheduler.add_job(gm.run, github_run_schedule['trigger'], hour=github_run_schedule['hour'],
                      minute=github_run_schedule['minute'], timezone='Asia/Shanghai')
    scheduler.add_job(send, push_schedule['trigger'], hour=push_schedule['hour'],
                      minute=push_schedule['minute'], timezone='Asia/Shanghai')
    scheduler.start()
