#!/usr/bin/env bash

# Arg 1 ($1): cloud type
# Arg 2 ($2): bucket (S3) name

sudo apt update
sudo apt -y upgrade
sudo apt -y install git
cd /var
sudo mkdir www
sudo chmod 777 www/
cd www/
git clone https://github.com/julienpiguet/CloudSys.git
cd CloudSys/testapp/backend/
chmod +x deploy_python.sh 
sudo ./deploy_python.sh $1 $2