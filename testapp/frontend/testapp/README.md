# testapp

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Deploy
Deploy frontend on an Ubuntu server

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
cd CloudSys/testapp/frontend/testapp
sudo npm install
```

### Config and build

```Bash
cd /var/www/CloudSys/testapp/frontend/testapp
vi src/config.js
```
Set the backend server
```Javascript
module.exports = {
    API_LOCATION: "CHANGE_TO_YOUR_BACKEND_IP_ADDR_OR_HOSTNAME"
}
```

Build
```Bash
npm run build
```


### Install web server

```Bash
sudo apt install nginx
cd /etc/nginx/sites-available/
sudo mv default default.bak
cp /var/www/CloudSys/testapp/frontend/testapp/nginx-default.conf default
vi default
```

Edit server name
```Bash
...
server_name CHANGE_TO_YOUR_SERVER_IP_ADDR_OR_HOSTNAME;
...
```
Save and close file (-> :wq )

Restart nginx
```Bash
sudo systemctl restart nginx
sudo systemctl status nginx
```
The app is now available at http://IP_ADDR/ (port 80)