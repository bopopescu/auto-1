
# My own .bashrc file
#11111
# If not running interactively, don't do anything
# [ -z "$PS1" ] && return

# alias ls='ls --color=always -F --group-directories-first'
# alias lo="ls -lha --color=always -F --group-directories-first | awk '{k=0;for(i=0;i<=8;i++)k+=((substr(\$1,i+2,1)~/[rwx]/)*2^(8-i));if(k)printf(\"%0o \",k);print}'"
# alias fact="elinks -dump randomfunfacts.com | sed -n '/^| /p' | tr -d \|"

# if [ -f /etc/bashrc ]; then
#     . /etc/bashrc   # --> Read /etc/bashrc, if present.
# fi

# shopt -s cdspell          # autocorrects cd misspellings
# shopt -s checkwinsize     # update the value of LINES and COLUMNS after each command if altered

# date

# export PS1="\[\e[1;32m\][\t] \u:\$(pwd)\n$ \[\e[m\]"

# .zshrc和.bashrc里面设置pubrc是bash和zsh公用的加载的rc, 可以把公用source的文件, 加载的目录, 都放到这儿
# mypath.sh里面是路径, 自己的脚本放到已经加载的pubkit目录里去
# 这个文件是函数, 自己的函数可以放在这里, 会被source
# 其他要source的文件也放在这里.
# ae修改.zsh/文件夹下面的alias文件
# lae修改pubkit下面的alias文件, 这两个文件都会被source. 但是是在不同的git目录里. 以后考虑合并. 使用submodule形式.
# fe修改本文件, 添加函数
# pubkit进入pubkit, 添加脚本.

############################ MOTD ###########################################


# figlet -f slant lhr auto # ascii 横幅, 漂亮, -c 居中. -ct 右对齐的样子. -f 字体, 不太管用.
#
# HOSTNAME=`uname -n`
# KERNEL=`uname -r`
# CPU=`uname -p`
# ARCH=`uname -m`
# # The different colours as variables
# W="\033[01;37m"
# B="\033[01;34m"
# R="\033[01;31m"
# X="\033[00;37m"
#
# echo -e "$R#===================================================#"
# echo -e  "$W Welcome $B $USER $W to $B $HOSTNAME"
# echo -e  "$R ARCH   $B= $ARCH"
# echo -e  "$R KERNEL $B= $KERNEL"
# echo -e  "$R CPU    $B= $CPU"
# echo -e  "$R#==================================================#"
#
# fortune | cowsay -n

############################ ALIAS ###########################################

# my alias
alias fuck='eval $(thefuck $(fc -ln -1 | tail -n 1)); fc -R'
# alias cp="cp -i"
alias o=open
alias c=c

# alias r=r

MY_EDITOR=atom

alias v='vagrant'
alias git='hub'

alias bi='brew install'
alias bs='brew search'
alias yi='sudo yum install'
alias ys='sudo yum search'

# 子shell里面alias都失效, 是的. alias不可以被export

# alias pubrc='cd $CONF/pubrc'
# alias pubkit='cd $AUTO/pubkit'
# alias mac='cd $AUTO/prikit/mac'
# alias linux='cd $AUTO/prikit/linux'
# alias remote='cd $AUTO/prikit/remote'
# alias labkit='cd $AUTO/labkit'
# alias prikit='cd $AUTO/prikit'

alias math='/Applications/Mathematica.app/Contents/MacOS/MathKernel'
alias E='/usr/local/Cellar/emacs-mac/emacs-24.4-mac-5.3/Emacs.app/Contents/MacOS/Emacs'
# alias e='emacsclient '

# OS X
alias qlf='qlmanage -p '

#alias mplayerx='open -a /Applications/MPlayerX.app --args -name'
#alias gs=gs
alias gfortran-4.2=gfortran


############################ FUNCTIONS ###########################################

function c(){

  cd $1 &&ls
}

function cd_apache(){
    # cd to apache www folder
    if [[ $OS_NAME == CYGWIN ]]; then
        cd /var/www/html
    elif [[ $OS_NAME == Darwin ]]; then
        cd /Library/WebServer/Documents
    else
        cd /var/www/html
    fi
}
function config_apache(){
  # config apache , apache config file
    if [[ $OS_NAME == Darwin ]]; then
        sudo vim /etc/apache2/httpd.conf
    # else

    fi
}
function restart_apache(){
  # apache restart
    if [[ $OS_NAME == Darwin ]]; then
      sudo  apachectl restart
    fi
}
function cd_nginx(){
  # cd to nginx www folder
    if [[ $OS_NAME == Darwin ]]; then

        cd  /usr/local/Cellar/nginx/1.6.2/html
    fi

}
function config_nginx(){
  # config nginx, open nginx config file
    if [[ $OS_NAME == Darwin ]]; then
        sudo vim /usr/local/etc/nginx/nginx.conf
    fi

}
function restart_nginx(){
  # nginx restart
    if [[ $OS_NAME == Darwin ]]; then
        nginx -s stop
        nginx
    fi

}



## =========


function aria(){
# aria download software
    if [ $# = 0 ]
    then
        aria2c --conf-path=/Users/lhr/.aria2/aria2.conf -D
    fi
    case $1 in
        start )
            aria2c --conf-path=/Users/lhr/.aria2/aria2.conf -D;;
        s )
            pkill aria2;;
        r )
            pkill aria2
            aria start;;
        f )
            open http://localhost/yaaw/index.html;;
        d )
            open file:///Users/lhr/downloads/aria2;;
    esac
}
## ==============

function count_project_lines(){
  if [[ $1 = "--help" ]]; then
    echo "count_project_words <surfix>  : to count project lines by the surfix, default surfix is py"
  fi

  surfix=$1
  # default value if surfix is not assigned
  surfix=${surfix:-py}
  find . -name "*.$surfix" |xargs wc -l {}\;
}


function ask(){
  #
    echo -n "$@" '[y/n] ' ; read ans
    case "$ans" in
        y*|Y*) return 0 ;;
        *) return 1 ;;
    esac
}

function extract(){
  # unzip , tar -zfx
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xvjf $1     ;;
            *.tar.gz)    tar xvzf $1     ;;
            *.bz2)       bunzip2 $1      ;;
            *.rar)       unrar x $1      ;;
            *.gz)        gunzip $1       ;;
            *.tar)       tar xvf $1      ;;
            *.tbz2)      tar xvjf $1     ;;
            *.tgz)       tar xvzf $1     ;;
            *.zip)       unzip $1        ;;
            *.Z)         uncompress $1   ;;
            *.7z)        7z x $1         ;;
            *)           echo "'$1' cannot be extracted via >extract<" ;;
        esac
    else
        echo "'$1' is not a valid file!"
    fi
}

# Creates an archive (*.tar.gz) from given directory.
function maketar() { tar cvzf "${1%%/}.tar.gz"  "${1%%/}/"; }
# tar

# Create a ZIP archive of a file or folder.
function makezip() { zip -r "${1%%/}.zip" "$1" ; }
# zip

function my_ps() { ps $@ -u $USER -o pid,%cpu,%mem,time,command,ppid ; }
# ps
function pp() { my_ps f | awk '!/awk/ && $0~var' var=${1:-".*"} ; }
# pp
function killps()
# kill by process name
{
    local pid pname sig="-TERM"   # default signal
    if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
        echo "Usage: killps [-SIGNAL] pattern"
        return;
    fi
    pattern=$1
    if [ $# = 2 ]; then sig=$1 pattern=$2; fi
    for pid in $(my_ps| awk '!/awk/ && $0~pat { print $1 }' pat=$pattern )
    do
        pname=$(my_ps | awk '$1~var { print $5 }' var=$pid )
        if ask "Kill process $pid <$pname> with signal $sig?"
            then kill $sig $pid
        fi
    done
}

function dataurl()
# dataurl
{
    local mimeType=$(file -b --mime-type "$1")
    if [[ $mimeType == text/* ]]; then
        mimeType="${mimeType};charset=utf-8"
    fi
    echo "data:${mimeType};base64,$(openssl base64 -in "$1" | tr -d '\n')"
}


#### ff command

[ $(uname -s | grep -c CYGWIN) -eq 1 ] && OS_NAME="CYGWIN" || OS_NAME=`uname -s`
function pclip() {

    if [[ $OS_NAME == CYGWIN ]]; then
        putclip $@;
    elif [[ $OS_NAME == Darwin ]]; then
        pbcopy $@;
    else
        if [ -x /usr/bin/xsel ]; then
            xsel -ib $@;
        else
            if [ -x /usr/bin/xclip ]; then
                xclip -selection c $@;
            else
                echo "Neither xsel or xclip is installed!"
            fi
        fi
    fi
}

function ff()
  # find file in current folder
{
    local fullpath=$*
    local filename=${fullpath##*/} # remove "/" from the beginning
    filename=${filename##*./} # remove  ".../" from the beginning
    echo file=$filename
    #  only the filename without path is needed
    # filename should be reasonable
    local cli=`find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print | percol`
    echo ${cli}
    echo -n ${cli} |pclip;
}

# alias percol='percol --match-method regex'

# alias percol='percol --eval="percol.view.prompt_on_top=False" --initial-index=last --reverse'
alias percol='percol --result-bottom-up --prompt-bottom'
# because percol can switch search method dynamicly, this alias is not needed now.

# #### zsh version of ppgrep and ppkill

function ppgrep() {
  # ppgrep
    if [[ $1 == "" ]]; then
        PERCOL=percol
    else
        PERCOL="percol --query $1"
    fi
    ps aux | eval $PERCOL | awk '{ print $2 }'
}

function ppkill() {
  # ppkill
    if [[ $1 =~ "^-" ]]; then
        QUERY=""            # options only
    else
        QUERY=$1            # with a query
        [[ $# > 0 ]] && shift
    fi
    ppgrep $QUERY | xargs kill $*
}

### zsh history search

function exists { which $1 &> /dev/null }
#
local tac
exists gtac && tac="gtac" || { exists tac && tac="tac" || { tac="tail -r" } }

if exists percol; then
    function percol_select_history() {
      # command history
        BUFFER=$(fc -l -n 1 | eval $tac | percol --query "$LBUFFER")
        CURSOR=$#BUFFER         # move cursor
        zle -R -c               # refresh
    }

    # zle -N percol_select_history
    # bindkey '^R' percol_select_history  # great binding keys from zsh to percol
fi

function teamocil_open_project(){
  # teamocil open project
  if [[ $1 == "" ]]; then
      PERCOL="percol"
  else
      PERCOL="percol --query $1"
  fi
  projects=`ls ~/.teamocil|while read i;do echo ${i%.yml};done`
  descriptions=`ls ~/.teamocil|while read i;do sed -n '/name/p' ~/.teamocil/$i;done`
  sessions=$(paste <(echo $projects) <(echo $descriptions))
  ans=$(echo $sessions|eval $PERCOL)
  project=$(echo $ans|cut -f1)
  teamocil $project
}

###########################################

function z(){
  # cd to recent or favarite directory
  if [[ $1 == "" ]]; then
      PERCOL=percol
  else
      PERCOL="percol --query $1"
  fi
  local tac
  exists gtac && tac="gtac" || { exists tac && tac="tac" || { tac="tail -r" } }

  folder=`cat <(cat $AUTO/etc/fav_folders) <(fasd -d|awk '{print $2}'|eval $tac)  |eval $PERCOL`
  cd $folder
}

function f(){
  # open recent and favarite files
  arg=$1
  if [[ $1 == "" ]]; then
      PERCOL="percol"
  else
      PERCOL="percol --query $1"
  fi
  # local cli=`find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print | percol`
  # ff=(find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print)
  # <(mdfind -onlyin . f -name $arg)

  run=$(cat <(fasd -f |eval $tac |awk '{print $2}') <(echo template)|eval $PERCOL)
  if [ $run = 'template' ];then
    template_list=$(ls ~/_env/templates)
    template=$(echo $template_list|eval $PERCOL)
    echo "please input the new target name:"
    read name
    run="cp -r ~/_env/templates/$template ./$name"
    eval $run
  else
    $MY_EDITOR $run
  fi
}
function bind_f(){
  # open recent and favarite files
  arg=$1
  if [[ $1 == "" ]]; then
      PERCOL="percol"
  else
      PERCOL="percol --query $1"
  fi
  # local cli=`find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print | percol`
  # ff=(find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print)
  # <(mdfind -onlyin . f -name $arg)
  #

  run=$(cat <(fasd -f |eval $tac |awk '{print $2}') <(echo template)|eval $PERCOL)
  if [ $run = 'template' ];then
    template_list=$(ls ~/_env/templates)
    template=$(echo $template_list|eval $PERCOL)
    run="cp -r ~/_env/templates/$template ./"
  fi
  BUFFER=`echo $run`
  CURSOR=$#BUFFER         # move cursor
  zle -R -c               # refresh
}
zle -N bind_f
bindkey '^F' bind_f  # great binding keys from zsh to percol

# function s(){
#   # list functions and commands
#   if [[ $1 == "" ]]; then
#       PERCOL="percol"
#   else
#       PERCOL="percol --query $1"
#   fi
#   run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
#   # his=$(fc -l -n 1 | eval $tac | percol --query "$LBUFFER")
#
#   eval $run
# }
# function bind_s(){
#   # list functions and commands
#   if [[ $1 == "" ]]; then
#       PERCOL="percol"
#   else
#       PERCOL="percol --query $1"
#   fi
#   his=$(fc -l -n 1 | eval $tac )
#   run=$(cat <(python $AUTO/rc/helper/option_list.py) <(echo $his)|eval $PERCOL|awk '{print $1}')
#
#   # $run
#   BUFFER=`echo $run`
#   CURSOR=$#BUFFER         # move cursor
#   zle -R -c               # refresh
#
# }
# zle -N bind_s
# bindkey '^R' bind_s  # great binding keys from zsh to percol


# function r(){
#   # config afp and commands / edit or creat
#
#   if [[ $1 == "" ]]; then
#       PERCOL="percol"
#   else
#       PERCOL="percol --query $1"
#   fi
#   his=$(fc -l -n 1 | eval $tac )
#   run=$(cat <(python $AUTO/rc/helper/option_list.py) <(echo $his)|eval $PERCOL)
#   run=${run%\#*}
#   if [ $run = 'afp.sh' ]; then
#     $MY_EDITOR $AUTO/rc/afp.sh
#   elif [ $run = 'create' ]; then
#     read name
#     cp -i ~/_env/templates/command $AUTO/commands/$name && $MY_EDITOR $AUTO/commands/$name
#   elif [ $run = 'cdto' ]; then
#     cd $AUTO/commands
#   elif [ $run = 'edit' ]; then
#     run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
#     if [ $(dirname `which $run` 2>/dev/null) = $AUTO/commands  ];then
#       $MY_EDITOR $AUTO/commands/$run
#     else
#       $MY_EDITOR $AUTO/rc/afp.sh
#     fi
#   else
#     # BUFFER=`echo $run`
#     # CURSOR=$#BUFFER         # move cursor
#     # zle -R -c               # refresh
#     eval $run
#   fi
# }

function bind_r(){
  # config afp and commands / edit or creat

  if [[ $1 == "" ]]; then
      PERCOL="percol"
  else
      PERCOL="percol --query $1"
  fi
  his=$(fc -l -n 1 | eval $tac )
  fc_list=$(python $AUTO/rc/helper/fc_list.py)
  option_list=$(python $AUTO/rc/helper/option_list.py)
  run=$(cat <(echo $option_list) <(echo $his) <(echo $fc_list)|eval $PERCOL)

  desc=$(echo $run|awk -F'\t' '{print $2}')
  run=$(echo $run|awk -F'\t' '{print $1}')
  run=$(echo $run|sed 's/ *$//g')

  if [ $run = 'afp.sh' ]; then
    $MY_EDITOR $AUTO/rc/afp.sh
  elif [ $run = 'fc' ]; then
      run=$(cat <(echo $fc_list)|eval $PERCOL)

      desc=$(echo $run|awk -F'\t' '{print $2}')
      run=$(echo $run|awk -F'\t' '{print $1}')
      run=$(echo $run|sed 's/ *$//g')
      if [ $(echo $desc|awk '/invoker/{print 1}') ];then
          subcommand=$($run -h|sed '1,5d'|percol)
          subcommand=$(echo $subcommand|sed 's/^ *//g'|awk '{printf $1}')
          BUFFER="$run $subcommand"
          CURSOR=$#BUFFER         # move cursor
          zle -R -c
          # eval "$run $subcommand"
      else
        BUFFER=`echo $run`
        CURSOR=$#BUFFER         # move cursor
        zle -R -c               # refresh
        # eval $run
      fi

  elif [ $run = 'create' ]; then
    tp=$(ls ~/_env/templates |eval $PERCOL)
    BUFFER="cp -i ~/_env/templates/$tp $AUTO/commands/$name"
    CURSOR=$#BUFFER         # move cursor
    zle -R -c               # refresh
  elif [ $run = 'delete' ]; then
    run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
    if [ $(dirname `which $run`) = $AUTO/commands  ];then
      BUFFER="rm -i $AUTO/commands/$run"
      CURSOR=$#BUFFER         # move cursor
      zle -R -c               # refresh
    else
      $MY_EDITOR $AUTO/rc/afp.sh
    fi
  elif [ $run = 'cdto' ]; then
    cd $AUTO/commands
  elif [ $run = 'edit' ]; then
    run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
    if [ $(dirname `which $run`) = $AUTO/commands  ];then
      $MY_EDITOR $AUTO/commands/$run
    else
      $MY_EDITOR $AUTO/rc/afp.sh
    fi

  elif [ `echo $desc|awk '/invoker/{print 1}'` ];then
      subcommand=$($run -h|sed '1,5d'|percol)
      subcommand=$(echo $subcommand|sed 's/^ *//g'|awk '{printf $1}')
      BUFFER="$run $subcommand"
      CURSOR=$#BUFFER         # move cursor
      zle -R -c
  else
    BUFFER=`echo $run`
    CURSOR=$#BUFFER         # move cursor
    zle -R -c               # refresh

    # eval $run
  fi
}

zle -N bind_r
bindkey '^R' bind_r  # great binding keys from zsh to percol



function r(){
  # config afp and commands / edit or creat

  if [[ $1 == "" ]]; then
      PERCOL="percol"
  else
      PERCOL="percol --query $1"
  fi
  his=$(fc -l -n 1 | eval $tac )
  fc_list=$(python $AUTO/rc/helper/fc_list.py)
  option_list=$(python $AUTO/rc/helper/option_list.py)
  run=$(cat <(echo $option_list)  <(echo $fc_list) <(echo $his)|eval $PERCOL)

  desc=$(echo $run|awk -F'\t' '{print $2}')
  run=$(echo $run|awk -F'\t' '{print $1}')
  run=$(echo $run|sed 's/ *$//g')

  if [ $run = 'afp.sh' ]; then
    $MY_EDITOR $AUTO/rc/afp.sh
  elif [ $run = 'fc' ]; then
      run=$(cat <(echo $fc_list)|eval $PERCOL)

      desc=$(echo $run|awk -F'\t' '{print $2}')
      run=$(echo $run|awk -F'\t' '{print $1}')
      run=$(echo $run|sed 's/ *$//g')
      if [ `echo $desc|awk '/invoker/{print 1}'` ];then
          subcommand=$($run -h|sed '1,5d'|percol)
          subcommand=$(echo $subcommand|sed 's/^ *//g'|awk '{printf $1}')
          # BUFFER="$run $subcommand"
          # CURSOR=$#BUFFER         # move cursor
          # zle -R -c
          eval "$run $subcommand"
      else
        # BUFFER=`echo $run`
        # CURSOR=$#BUFFER         # move cursor
        # zle -R -c               # refresh
        eval $run
      fi

  elif [ $run = 'create' ]; then
    tp=$(ls ~/_env/templates |eval $PERCOL)
    # BUFFER="cp -i ~/_env/templates/$tp $AUTO/commands/$name"
    # CURSOR=$#BUFFER         # move cursor
    # zle -R -c               # refresh
    echo "please input the new target name:"
    read name
    cp -i ~/_env/templates/$tp $AUTO/commands/$name
    $MY_EDITOR $AUTO/commands/$name
  elif [ $run = 'delete' ]; then

    run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
    if [ $(dirname `which $run`) = $AUTO/commands  ];then
      rm -i $AUTO/commands/$run
    else
      $MY_EDITOR $AUTO/rc/afp.sh
    fi

  elif [ $run = 'cdto' ]; then
    cd $AUTO/commands
  elif [ $run = 'edit' ]; then
    run=$(python $AUTO/rc/helper/fc_list.py|eval $PERCOL|awk '{print $1}')
    if [ $(dirname `which $run`) = $AUTO/commands  ];then
      $MY_EDITOR $AUTO/commands/$run
    else
      $MY_EDITOR $AUTO/rc/afp.sh
    fi

  elif [ `echo $desc|awk '/invoker/{print 1}'` ];then
      subcommand=$($run -h|sed '1,5d'|percol)
      subcommand=$(echo $subcommand|sed 's/^ *//g'|awk '{printf $1}')
      # BUFFER="$run $subcommand"
      # CURSOR=$#BUFFER         # move cursor
      # zle -R -c
      eval "$run $subcommand"

  else
    # BUFFER=`echo $run`
    # CURSOR=$#BUFFER         # move cursor
    # zle -R -c               # refresh
    eval $run
  fi
}


function t(){
  # tmux or attach or teamocil
  if [ $TMUX ] ; then
    teamocil_open_project
  else
    pattach &&  tmux
  fi
}



### tmux pattach
function pattach() {

    if [[ $1 == "" ]]; then
        PERCOL=percol
    else
        PERCOL="percol --query $1"
    fi

    sessions=$(tmux ls)
    [ $? -ne 0 ] && return

    session=$(echo $sessions | eval $PERCOL | cut -d : -f 1)
    if [[ -n "$session" ]]; then
        tmux att -t $session
    fi
}
# export -f pattach





# function detached_a(){
#
#   if [[ $1 == "" ]]; then
#       PERCOL=percol
#   else
#       PERCOL="percol --query $1"
#   fi
#
#   invokers=`ls $AUTO/invokers`
#   descriptions=`echo $invokers|xargs -I% sed -n '2p' $AUTO/invokers/%`
#   # 上面这句是bash不兼容的, 数组问题.
#
#   # funcs=$(for i in (d m); do echo $i;done)
#   funcs="\nd\nm\nmt\n^P"
#   fdesc="\n# cd to recent folder\n# tmux\n# tmux attach\n# list my commands\n"
#
#   invokers=`echo $invokers  $funcs`
#   descriptions=`echo $descriptions $fdesc`
#
#   ans=`paste <(echo $invokers) <(echo $descriptions)|eval $PERCOL`
#   run=$(awk '{print $1}' <(echo $ans))
#   eval $run
# }


#
# function list_my_commands(){
#   # list my commands
#   if [[ $1 == "" ]]; then
#       PERCOL=percol
#   else
#       PERCOL="percol --query $1"
#   fi
#   # todo: 根据gitignore来判断
#   command_list=`ls $AUTO/commands|while read i ;do [[ ${i/pyc/} == $i ]]&&echo $i;done`
#   descriptions=`echo $command_list|xargs -I% sed -n '1p' "$AUTO/commands/%"`
#
#   ans=`paste <(echo $command_list) <(echo $descriptions)|eval $PERCOL`
#   run=$(awk '{print $1}' <(echo $ans))
#
#   BUFFER=`echo $run`
#   CURSOR=$#BUFFER         # move cursor
#   zle -R -c               # refresh
# }

# zle -N list_my_commands
# bindkey '^P' list_my_commands  # great binding keys from zsh to percol
# bindkey '^F' list_my_commands  # great binding keys from zsh to percol

############################ PATH ###########################################

#RUBY AND PYTHON
# export PATH=~/anaconda2/bin:$PATH
export PATH=$HOME/.rvm/bin:/usr/local/bin:$PATH
export PATH=~/.local/bin:$PATH
source /usr/local/bin/virtualenvwrapper.sh
source /usr/local/bin/activate.sh

# zsh下面脚本无效, 手动加
export PATH=/Users/lhr/.rvm/rubies/ruby-2.2.3/bin:$PATH
# [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

# ON GOING PROJECT
export PYTHONPATH=$SITES/91/labkit:$PYTHONPATH
export PYTHONPATH=~/_env/apps/stock:$PYTHONPATH
# export PYTHONPATH=~/_env/lib/general:$PYTHONPATH
export PYTHONPATH=$SITES/91/general:$PYTHONPATH

# 加载lhrkits里面所有kit的目录
source $AUTO/init_kits.sh

#ANSIBLE
# export ANSIBLE_INVENTORY=$AUTO/ansible/hosts
# export ANSIBLE_ROLES=$AUTO/ansible/centos/roles


# export PATH=~/.local/bin:~/anaconda/bin:/usr/local/bin:$PATH
export PATH=$PATH:/Applications/Osmo4.app/Contents/MacOS/:/Applications/Mkvtoolnix-7.2.0.app/Contents/MacOS/
export PATH=$PATH:/Applications/Araxis\ Merge.app/Contents/Utilities

# homebrew ustc source
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles

# proxy 设置
export http_proxy=`proxy-config -h`
export https_proxy=`proxy-config -s`
export ftp_proxy=`proxy-config -f`
