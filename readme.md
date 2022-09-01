# EXP-Monitoring
从 Github 上获取最新漏洞信息，并对仓库标星和数量进行持续监控，对短期内标星数量快速提升和创建仓库数量快速增加的 CVE 漏洞进行提醒。
## 安装
### 下载安装
```shell
cd /usr/share/
git clone https://github.com/45qq/EXP-Monitoring.git
cd EXP-Monitoring
python3 -m pip install -r requirements.txt
```
### 完善 config.yaml 配置
需要在 config.yaml 中配置：
 - github token
 - Server酱的 send_key
 - mysql 数据库主机、用户、密码

配置 github token 和 Server酱的 send_key。
```yaml
github_monitor_config:
  token: ghp_15phroQOJtruJIaNPqa2614pYWwaxxxxxx
......
push_config:
  server_chan:
    send_key: SCT63558ToWsvMZ0vUbc76WIhxxxxxx
......
```
使用 mysql 数据库，mysql 请自行安装，需要 5.6 以上的版本。  
需要修改 mysql 数据库用户名和密码：
```yaml
mysql_config:
  db: 'exp-monitoring'
  host: 'localhost'
  port: 3306
  user: 'root'
  password: 'root'
```
### 配置为为 Linux 服务
```shell
# 复制 exp-monitoring.service.example 文件到指定目录下
cp ./exp-monitoring.service.example /usr/lib/systemd/system/exp-monitoring.service
# 开启服务
service exp-monitoring start
# 查看服务状态
systemctl status exp-monitoring.service
# 设置开机自启动
systemctl enable exp-monitoring.service

# 关闭服务
service exp-monitoring stop
# 重启服务
service exp-monitoring restart
```
## config.yaml 配置内容
```yaml
github_monitor_config:
  # 配置 github token （在 https://github.com/settings/tokens/new 生成）。
  token:
  # 设置标星和仓库数量的监控时长（暂未实现）。
  monitoring_time: 5
  # 配置监控的关键词，{year}会替换为最新的年份
  # 如果 {year} 为 2022 年，那么 {year-1} 为 2021 年，依此类推最大为 {year-10}。
  # 也可以使用其它关键词，如：RCE 等。
  update_key:
    - cve-{year}
    - cve-{year_1}
    - cve-{year_2}
    - cve-{year_3}
    - cve-{year_4}
    - cve-{year_5}
    - cve-{year_6}
  # 是否启用精确匹配，启用后将只匹配仓库名，关闭将匹配配仓库名和描述。
  enable_exact_match: true
  # Github 推送过滤配置。
  push_config:
    # Github 更新推送的最低标星。
    lowest_star: 2
    # Github 标星监控，标星增长推送的最低标星。
    # 5，20，50 表示分别在仓库增长超过 5、20、50 星时推送，一个仓库有可能会推送三次。
    growth_warning_star:
      - 5
      - 20
      - 50
    # Github 仓库数量监控，仓库数量增长推送的最低标星。
    name_warning_count:
      - 3
      - 6

# mysql 数据库配置
# 需要 mysql 5.6 或以上的版本
mysql_config:
  db: 'exp-monitoring'
  host: 'localhost'
  port: 3306
  user: 'root'
  password: 'root'

# 推送配置
push_config:
  # Server酱推送配置
  server_chan:
    send_key:

# 计划任务配置
schedule:
  # github 运行计划任务配置
  github_run:
    # trigger 参数可以是: interval 或 cron
    # trigger: interval
    # hour: 1
    # 表示每 1 小时运行一次
    # trigger: cron
    # hour: 5,7,9,11-13
    # minute: 0
    # 表示在每天的 5、7、9点整和 11、12、13 点整运行
    trigger: cron
    hour: 5,11,17,20,23
    minute: 0
  # 推送计划任务配置
  # 配置推送的时间，默认在 github 监控运行半小时后推送
  push:
    trigger: cron
    hour: 5,11,17,20,23
    minute: 30
```
## 效果
![e1](doc/e1.jpg)
![e2](doc/e2.jpg)
![e3](doc/e3.jpg)