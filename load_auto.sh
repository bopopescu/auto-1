#!/bin/zsh
# load all auto's path and source functions

# for dir_name in ` find $AUTO -maxdepth 1 -type d |grep -E  "kit$" `
# do
#     # echo $dir_name
#     if [ -f $dir_name/init_kit.sh ]; then
#         source $dir_name/init_kit.sh
#     fi
# done

RC=$AUTO/rc
INVOKERS=$AUTO/invokers
COMMANDS=$AUTO/commands

PATH=$RC:$INVOKERS:$COMMANDS:$PATH
for i in `ls $RC/*.sh 2>/dev/null`; do
  source $i
done

# zsh和bash加载顺序, 基础->公用->(zsh特别)->私有. 只有基础在conf里面, 后面都再auto里面. 不要再conf和auto分别分层, 这样太复杂. 就这样只一趟走过来.

# rc, invokers, commands内部平铺, 不存在子目录.
