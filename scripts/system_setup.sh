#!/bin/sh
sudo yum install -y gcc python-virtualenv python3 python3-devel sendmail mysql mariadb-server

sudo iptables -A INPUT -p tcp --dport 25 -j ACCEPT
