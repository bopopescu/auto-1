##!/bin/sh 
# 
# Resets the iptables to default values, in case you screw something up 
# while setting your rc.firewall up - as I did quite a few times;) 
# 
# Author: Oskar Andreasson 
# (c) of BoingWorld.com, use at your own risk, do whatever you please with 
# it as long as you don't distribute this with due credits to 
# BoingWorld.com

# 
# reset the default policies in the filter table. 
# 
/sbin/iptables -P INPUT ACCEPT 
/sbin/iptables -P FORWARD ACCEPT 
/sbin/iptables -P OUTPUT ACCEPT

# 
# reset the default policies in the nat table. 
# 
/sbin/iptables -t nat -P PREROUTING ACCEPT 
/sbin/iptables -t nat -P POSTROUTING ACCEPT 
/sbin/iptables -t nat -P OUTPUT ACCEPT

# 
# flush all the rules in the filter and nat tables. 
# 
/sbin/iptables -F 
/sbin/iptables -t nat -F

# 
# erase all chains that's not default in filter and nat table. 
# 
/sbin/iptables -X 
/sbin/iptables -t nat -X 


