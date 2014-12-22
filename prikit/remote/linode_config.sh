#!/bin/bash
#


#### ssh ####

mkdir ~/.ssh;chmod 700 ~/.ssh; touch ~/.ssh/authorized_keys; echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkFceJt56ZJcaCABNIoS6XsmxHOJoEMzfdEKqJtngWs/lxKPTHkhcw8hDHlEzgbxyk0Nqs/SOvsOlqphmqtzKZag5N5W1KOi8dG8Niw5OyT0jN7tJHQ3j2O3oELZ0xLNL9XyJMjZtTHgYgRkRJMvpTningJGyJgQkrZg+WqYOeswAvinWikaAbQ2Kf6u3HhoSGs2lx7q73h3WU497rKy/hxe9De+IRFdJOzPLTACwjWQ6v35iRbFsKDwt/uZNqfeGJpW7HS8Yggoqhs0ZeaOOHLTtOv1L1a8MujC96p/GjL2ttL1nTCzwFtRT9VlCS8ztPeZxftm6pbiECBlRm2eHH lhr@lhr-mbp.local">>~/.ssh/authorized_keys; chmod 644 ~/.ssh/authorized_keys;


echo "PubkeyAuthentication yes\nAuthorizedKeysFile      .ssh/authorized_keys\nPermitRootLogin yes\n">>/etc/ssh/sshd_config

#### yadr ####
cd ~
cat ~/.ssh/id_rsa.pub
git clone git@github.com:lhrkkk/dotfiles.git ~/.yadr

\curl -sSL https://get.rvm.io | bash -s stable --ruby --rails
apt-get install zsh

cd .yadr
rake install

#### pptpd vpn ####


apt-get update
apt-get install pptpd


sed -i 's/#localip 192.168.0.1/localip 192.168.217.1/' /etc/pptpd.conf
sed -i 's/#remoteip 1192.168.0.234-238,192.168.0.245/remoteip 192.168.217.234-238,192.168.217.245/' /etc/pptpd.conf


if [ ! `grep lhr /etc/ppp/chap-secrets` ]; then
    echo "lhr pptpd vsyouk *"  >>/etc/ppp/chap-secrets
fi

echo "ms-dns 8.8.8.8\nms-dns 8.8.4.4" >>/etc/ppp/options

sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

sysctl -p

/etc/init.d/pptpd restart
apt-get install iptables

iptables -t nat -A POSTROUTING -s 192.168.217.0/24 -o eth0 -j MASQUERADE
iptables-save > /etc/iptables.pptp

touch /etc/network/if-up.d/iptables
echo "#!/bin/sh\niptables-restore < /etc/iptables.pptp" >/etc/network/if-up.d/iptables
chmod +x /etc/network/if-up.d/iptables

mknod /dev/ppp c 108 0
