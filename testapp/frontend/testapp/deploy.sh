#!/usr/bin/env bash

sudo apt update

sudo apt -y install npm
sudo npm install -g n
n latest
n prune

cd /var/www/CloudSys/testapp/frontend/testapp
sudo npm install

echo "module.exports = { API_LOCATION: \"http://$1\" }" > /var/www/CloudSys/testapp/frontend/testapp/src/config.js

npm run build

sudo apt -y install nginx
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp /var/www/CloudSys/testapp/frontend/testapp/nginx-default.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx