# TestApp Backend

## Setup Dev

### Install Node and NPM
```Bash
sudo apt update
sudo apt install nodejs npm

node --version
v18.9.0

npm --version
8.19.1
```

### Install dependencies
```Bash
npm install
```

## Run

```Bash
node app.js
```

## Deploy
Deploy backend on an Ubuntu server

### Setup node
```Bash
sudo apt update
sudo apt upgrade
sudo apt install npm
sudo npm install -g n
n latest
n prune
node --version
```
restart shell if necessary

### Clone and init app
```Bash
cd /var/www/
sudo git clone https://github.com/julienpiguet/CloudSys.git
sudo chmod -R 777 CloudSys/
cd CloudSys/testapp/backend/
sudo npm install
```
### Setup as a service

```Bash
cd /var/www/CloudSys/testapp/backend/
sudo chmod +x app.js
sudo cp backendapp.service /etc/systemd/system/
sudo systemctl start backendapp
sudo systemctl status backendapp
```

### Install reverse proxy

```Bash
sudo apt install nginx
cd /etc/nginx/sites-available/
mv default default.bak
cp /var/www/CloudSys/testapp/backend/nginx-default.conf default
vi default
```
Edit server name
```Bash
...
server_name CHANGE_TO_YOUR_SERVER_IP_ADDR;
...
```
Save and close file (-> :wq )

Restart nginx
```Bash
sudo systemctl restart nginx
sudo systemctl status nginx
```
The app is now available at http://IP_ADDR/ (port 80)

(try http://IP_ADDR/element/all )

## Add new storage

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