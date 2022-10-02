#!/usr/bin/env bash

# Arg 1 ($1): backend address

sudo apt update
sudo apt -y upgrade
sudo apt -y install git
cd /var
sudo mkdir www
sudo chmod 777 www/
cd www/
git clone https://github.com/julienpiguet/CloudSys.git
cd CloudSys/testapp/frontend/testapp
chmod +x deploy.sh 
sudo ./deploy.sh $1