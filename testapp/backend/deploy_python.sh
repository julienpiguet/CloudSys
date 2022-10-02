#!/usr/bin/env bash

sudo apt update
sudo apt -y install python3 pip python3-venv
sudo apt -y install crudini

sudo apt install nginx
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp /var/www/CloudSys/testapp/backend/nginx-default.conf default

cd ./python

crudini --set config.ini DEFAULT StoreType $1
crudini --set config.ini $1 arg $2

python3 -m venv venv
source venv/bin/activate

pip install fastapi[all]
pip install uvicorn[standard]
pip install uuid
pip install google-cloud-storage
pip install exoscale
pip install gunicorn

deactivate

sudo cp pythonapp.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start pythonapp