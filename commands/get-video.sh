#!/usr/bin/env bash

flv_web_addr=$1
flv_dir=$HOME/Downloads/videos    #存放视频地址的位置
flvcd_page_file=/tmp/flv_page_file

wget -q -O $flvcd_page_file "http://www.flvcd.com/parse.php?format=high&kw=$flv_web_addr"
flvurls=( $(cat $flvcd_page_file | grep "<U>" | sed s/\<U\>//g) )  #取出所有片段的视频地址
flvtitles=( $(cat $flvcd_page_file | grep "<N>" | iconv -f gb2312 -t utf8 | sed -n "s/\s\{1,\}/_/g;s/<N>//gp") )  #取出所有片段的标题，将空格替换为下划线
nr_urls=${#flvurls[@]}

if [ $nr_urls -eq 0 ]
then
    echo "No videos found in this page :("
    exit 1
fi

for ((i=0; i<$nr_urls; i++))
do
    title=${flvtitles[$i]}
    url=${flvurls[$i]}
    echo "title: $title"
    echo "  url: $url"
    wget -U NoSuchBrowser/1.0 -O "$flv_dir/$title.flv" $url
done