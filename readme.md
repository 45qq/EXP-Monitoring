# EXP-Monitoring

从 Github 上获取最新漏洞信息，并对仓库标星和数量进行持续监控。

## 特点

一般从漏洞公布到出现 exp 的时间在15天以内，EXP-Monitoring 将从 Github 上获取漏洞信息，对持续监控一段时间（默认持续监控20天），记录这段时间内仓库的标星数量变化，对短期内标星数量快速上升和创建仓库数量快速增加的
CVE 漏洞将会被记录，最后对搜集到的漏洞信息进行过滤后推送。

- 持续监控标星和仓库数量变化
- 扫描和推送分离，支持自定义扫描计划和推送时间
- 推送过滤，过滤掉大量无用漏洞
- 支持推送类型： Server酱、邮件、钉钉
- 推送附带 CNNVD 中文描述

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
- 推送方式
- mysql 数据库主机、用户、密码

配置 github token
```yaml
github_monitor_config:
  # 配置 github token （在 https://github.com/settings/tokens/new 生成）。
  token: ghp_15phroQOJtruJIaNPqa2614pYWxxxxxxxxxxx
......
```

配置推送方式，Server酱的 send_key（也可以配置其它推送方式，选择一两个就行了）。
```yaml
# 推送配置
push_config:
  # Server酱推送配置
  server_chan:
    enable: true
    send_key: SCT63558ToWsvMZ0vUbcxxxxxxxxxxxxxx
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

### 启动

配置为为 Linux 服务后脚本会自动运行，不使用 Linux 服务则使用以下方式启动保持后台运行：
```shell
nohup python3 EXP-Monitoring.py &
```
启动后会进行数据库安装和 Github 数据初始化，完成后会从配置的推送方式发送一条初始化成功的通知信息，如果没有搜到则查看服务状态查看报错信息。

## 效果

<table>
	<tr>
        <td><img src="doc/e1.jpg" alt="e1"/></td>
        <td><img src="doc/e2.jpg" alt="e2"/></td>
        <td><img src="doc/e3.jpg" alt="e3"/></td>
        <td><img src="doc/e4.jpg" alt="e3"/></td>
    </tr>
    <tr>
        <td><img src="doc/e5.jpg" alt="e1"/></td>
        <td><img src="doc/e6.jpg" alt="e2"/></td>
        <td><img src="doc/e7.png" alt="e7"/></td>
    </tr>
</table>