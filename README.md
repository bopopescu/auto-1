rc: run command 一开始就要加载和运行的command
invokes: 触发器
commands: 存放命令
私密信息去vault里面取.
平台相关的话, 用link, 可以写一个安装脚本.


关于python

全局的python需要安装的包, 重命名anaconda的deactivate避免和virtualenvwrapper冲突
pip install percol virtualenvwrapper autoenv  invoke autopep8 isort
mv ~/anaconda2/bin/deactivate ~/anaconda2/bin/conda-deactivate 


pip-tools必须在虚拟环境中安装, 不要安装到全局中. 避免pip-sync弄坏了全局的环境. 


