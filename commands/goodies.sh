## 有意思的命令
# yes #打印无数个 y, 可以回答一连串问题
# banner hello  # ascii 字符竖条幅
# figlet hello # ascii 横幅, 漂亮, -c 居中. -ct 右对齐的样子. -f 字体, 不太管用.
# figlet -f slant hello # ascii 横幅, 漂亮, -c 居中. -ct 右对齐的样子. -f 字体, 不太管用.
# toilet hello # ascii 横幅
# sudo echo `toilet -f bigmono9 -F gay HELLO`>/etc/motd # -f 设置元素类型, -F 设置颜色风格, 用 tab 补全可以列出选项
# 文字图片动画转 asciiart: http://www.asciiarts.net/
# http://ruletheweb.co.uk/figlet/ 有更多的字体风格, 推荐lildevel
# fortune  # 格言
# cal 9 1752  # 日历
# cowsay hello  # 萌牛说
# cowthink world # 萌牛想
# sl # 小火车
# gfactor #分解因数, linux下是factor
# who is i

## linux专用
# apt-get moo # 显示一些萌物
# apt-build moo # 同上
# aptitude moo
# aptitude -v moo
# aptitude -vv moo
# ...
# linuxlogo
# xeyes # 眼镜, x11
# oneko # 小猫, x11
# xev # 打印 x 事件



# motd
HOSTNAME=`uname -n`
KERNEL=`uname -r`
CPU=`uname -p`
ARCH=`uname -m`
# The different colours as variables
W="\033[01;37m"
B="\033[01;34m"
R="\033[01;31m"
X="\033[00;37m"
echo -e "$R#===================================================#"
echo -e  "$W Welcome $B $USER $W to $B $HOSTNAME"
echo -e  "$R ARCH   $W= $ARCH"
echo -e  "$R KERNEL $W= $KERNEL"
echo -e  "$R CPU    $W= $CPU"
echo -e  "$R#==================================================#"
fortune | cowsay -n

## 一些 atom插件
# atom 有 figlet 插件, 命令面板里面搜 figlet

# pangu 中英文文分词, atom插件

# isort, python import排序
# sort, line排序





# ${}做变量操作
# $(())数学运算
# $()提取命令结果

#
# xargs并行, -P2是开两个进程:
# ls|xargs -P2 -I% echo %
#
#
# dstat: iostat, vmstat, ifstat 三合一的工具, linux可用
# alias dstat='dstat -cdlmnpsy'
#
# 查看哪个进程占用端口
# netstat -lntp
#
#
# ()子shell, 常用于临时切换到某个目录种, 例如:
# # do something in current dir
# (cd /some/other/dir; other-command)
# # continue in original dir
#
# trash-cli删除到回收站
#
#
# mac上的trash-cli: http://www.makkintosshu.com/development#tools-osx
# https://github.com/morgant/tools-osx
#
#
# awk是excel, sed是行正则编辑器.
#
#
# 多看看ansible的模板, 另外如果要传变量给awk之类的, 可以先传递变量拼成的字符串, 然后再传给awk. 另外如果有什么技巧, 不要觉得自己一下子就记住了, 好记性不如烂笔头, 而且记下来以后可以复用.
