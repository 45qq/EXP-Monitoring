# EXP-Monitoring

从 Github 上获取最新漏洞信息，并对仓库标星和数量进行持续监控。

## 特点

一般从漏洞公布到出现 exp 的时间在15天以内，EXP-Monitoring 将从 Github 上获取漏洞信息，对持续监控一段时间（默认持续监控20天），记录这段时间内仓库的标星数量变化，对短期内标星数量快速上升和创建仓库数量快速增加的
CVE 漏洞将会被记录，最后对搜集到的漏洞信息进行过滤后推送。

- 持续监控标星和仓库数量变化
- 扫描和推送分离，支持自定义扫描计划和推送时间
- 推送过滤，过滤掉大量无用漏洞
- 支持推送类型： Server酱、邮件
- 推送附带 CNNVD 描述

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

## 效果

Server酱：
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
    </tr>
</table>