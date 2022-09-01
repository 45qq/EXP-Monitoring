# EXP-Monitoring
从 Github 上获取最新漏洞信息，并对仓库标星和数量进行持续监控。

## 安装
### 下载安装
```shell
git clone https://github.com/45qq/EXP-Monitoring.git
cd EXP-Monitoring
python3 -m pip install requirements.txt
```
### 完善 config.yaml 配置
在 config.yaml 中配置：
 - github token
 - Server酱的 send_key
 - mysql 数据库主机、账号、密码

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
```yaml
mysql_config:
  db: 'exp-monitoring'
  host: 'localhost'
  port: 3306
  user: 'root'
  password: '@123456z'
```
### 安装为 Linux 服务
```shell
# 复制 exp-monitoring.service.example 文件到指定目录下
cp ./exp-monitoring.service.example /usr/lib/systemd/system/exp-monitoring.service
# 开启服务
service exp-monitoring start
# 设置开机自启动
systemctl enable exp-monitoring.service

# 关闭服务
service exp-monitoring stop
# 重启服务
service exp-monitoring restart
```
