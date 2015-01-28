# outwall tools for linux

### usage
for example, 

  outwall_linux.py ~/.dropbox-dist/dropboxd &

outwall_linux.py is in ~/.yadr/mybin/linux

### infomations

This is the readme file of my outwall tools for linux

all file are placed in ~/.outwall

please install shadowsocks first:

    pip install shadowsocks

use shadowsocks for outwall

use proxychain-ng to connect to shadowsocks port to exec process through shadowsocks

## refs:

### proxychains-ng
https://github.com/rofl0r/proxychains-ng

*** Installation ***

  # needs a working C compiler, preferably gcc
  ./configure --prefix=/usr --sysconfdir=/etc
  make
  [optional] sudo make install
  [optional] sudo make install-config (installs proxychains.conf)

  if you dont install, you can use proxychains from the build directory
  like this: ./proxychains4 -f src/proxychains.conf telnet google.com 80


### shadowsocks client 

http://shadowsocks.org/en/config/quick-guide.html
https://wiki.archlinux.org/index.php/Shadowsocks_%28简体中文%29#.E5.AE.A2.E6.88.B7.E7.AB.AF

Shadowsocks accepts JSON format configs like this:

    {
        "server":"my_server_ip",
        "server_port":8388,
        "local_port":1080,
        "password":"barfoo!",
        "timeout":600,
        "method":"table"
    }

客户端
在config.json所在目录下运行sslocal即可；若需指定配置文件的位置：
    
    sslocal -c /etc/shadowsocks/config.json
注意: 有用户报告无法成功在运行时加载config.json，或可尝试手动运行：
    
    sslocal -s 服务器地址 -p 服务器端口 -l 本地端端口 -k 密码 -m 加密方法