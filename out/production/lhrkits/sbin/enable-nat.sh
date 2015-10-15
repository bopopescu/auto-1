sysctl net.ipv4.ip_forward=1
/sbin/iptables -t nat -A POSTROUTING  -s 192.168.1.0/24 -j MASQUERADE
