const { Store } = require('./Store.js');
const {Storage} = require('@google-cloud/storage');

class GoogleStore extends Store {
    

    constructor(bucketName) {
        super();
        this.storage = new Storage();
        this.bucketName = bucketName;
        this.bucket = this.storage.bucket(bucketName);
        
    }

    postItem(item) {
        
    }

    getAllItems() {

        return
    }
}

module.exports.GoogleStore = GoogleStore;