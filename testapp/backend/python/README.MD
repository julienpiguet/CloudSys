# TestApp Python Backend

## Setup Dev

### Install Python
```Bash
sudo apt update
sudo apt install nodejs npm

python3 --version
Python 3.8.10
```

### Install dependencies
```Bash
python3 -m pip install fastapi
python3 -m pip install uvicorn[standard]
python3 -m pip install uuid
```

## Run

```Bash
uvicorn app:app --reload --port 3000
```

## Deploy
Deploy backend on an Ubuntu server

### Setup node
```Bash
sudo apt update
sudo apt upgrade
sudo apt install python3 pip python3-venv
python3 -m pip install fastapi
python3 -m pip install uvicorn[standard]
python3 -m pip install uuid
python3 -m pip install google-cloud-storage
python3 -m pip install exoscale
```
restart shell if necessary

### Clone and init app
```Bash
cd /var/www/
sudo git clone https://github.com/julienpiguet/CloudSys.git
sudo chmod -R 777 CloudSys/
cd CloudSys/testapp/backend/python
```
### Setup as a service

```Bash
sudo apt -y install python3 pip python3-venv

crudini --set config.ini DEFAULT StoreType NAME
crudini --set config.ini StoreType arg BUCKET_NAME

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
```
### Install reverse proxy

```Bash
sudo apt install nginx
cd /etc/nginx/sites-available/
mv default default.bak
cp /var/www/CloudSys/testapp/backend/nginx-default.conf default
```

Restart nginx
```Bash
sudo systemctl restart nginx
sudo systemctl status nginx
```
The app is now available at http://IP_ADDR/ (port 80)

(try http://IP_ADDR/element/all )

## Add new storage

### add Exoscale API KEY 
please create an api key in IAM in Exoscale  

$ export EXOSCALE_API_KEY="EXOxxxxxxxxxxxxxxxxx" EXOSCALE_API_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

### Create an Object
Create a new file and an object that extends Store
```Javascript
class NewStore extends Store {
...
}
module.exports.NewStore = NewStore;
```

The following functions are inheritate and can be override:
```Javascript
    connect(url) { ... } -> boolean

    isConnected() { ... } -> boolean

    postItem(item) { ... } -> void

    getItemById(id) { ... } -> {id: String, title: String, img: String}

    getAllItems() { ... } -> [{id: String, title: String, img: String},...]
```

### Add Store to builder
In the StoreBuilder.js import the new Store
```Javascript
const { NewStore } = require('./NewStore.js');
```
and add it in the Map
```Javascript
stores.set("newstore", (params) => new NewStore(params))
```