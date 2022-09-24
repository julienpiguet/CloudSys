const { Store } = require('./Store.js');
var fs = require('fs');

class LocalStore extends Store {

    constructor(filename) {
        super();
        this.filename = filename;
        fs.open(filename, 'r', function (fileExists, file) {
            if (fileExists) {
                fs.writeFile(filename, JSON.stringify({ data: [] }), (err) => {
                    if (err) console.error(err)
                });
            }
        });

    }

    postItem(item) {
        var f = JSON.parse(fs.readFileSync(this.filename).toString());
        f.data.push(item)
        fs.writeFileSync(this.filename, JSON.stringify(f));
    }

    getAllItems() {
        var f = JSON.parse(fs.readFileSync(this.filename).toString());
        return f.data
    }
}

module.exports.LocalStore = LocalStore;