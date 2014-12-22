# export PATH=$HOME/.yadr/mybin:$PATH
dir_list=(pubkit labkit)

for dir_name in ${dir_list[@]}
do
    # echo $dir_name
    source dir_name/.kitpath
    export PATH=$HOME/.yadr/mybin/$dir_name:$PATH
    # echo $HOME/.yadr/mybin/$dir_name
done

# export PATH=$HOME/.yadr/mybin:$HOME/.yadr/mybin/pub:$HOME/.yadr/mybin/remote:$HOME/.yadr/mybin/mac:$PATH