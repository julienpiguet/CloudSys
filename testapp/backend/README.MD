# TestApp Backend

## Setup

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