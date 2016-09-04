# 基于 Flask 开发的大屏消息分发系统

## 功能与系统结构

电视等大屏设备作为 Raspberry Pi 的显示器，通过 HDMI 线连接。Raspberry Pi 接通网站，并在其上运行 Flask Web App。

局域网中的客户端机器通过浏览器访问 Flask Web App，用户通过浏览器分发图片和消息，分发的图片和消息实时在大屏上显示。

### 主要功能

+ 用户登录注销功能
+ 图片文件和消息发布功能


## 运行环境
+ 运行硬件：显示器大屏 + Raspberry Pi
+ 软件环境：Raspbian + Python2.7 + Flask 0.11.1 + Chromium


## 安装

+ 安装 Virtualenv
+ git clone 源码
+ chmod a+x startup.sh
+ 运行 startup.sh
+ 如果要开机自动启动，在 Rasbian LXDE 系统中：

```sh
$ sudo vi /etc/xdg/lxsession/LXDE-pi/autostart
```

然后将启动脚本添加进去，如下：

```conf
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@lxterminal
@leafpad
@xscreensaver -no-splash@
@bash /home/pi/workspace/screen-message-delivery/startup.sh
```

或者也可以将启动脚本添加到 `~/.config/lxsessionn/LXDE/autostart` 文件中。


## 运行情况

### 首页

### 登录页

### 消息分发页

### 消息显示页
