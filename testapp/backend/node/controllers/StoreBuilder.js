const { LocalStore } = require('./LocalStore.js');

const stores = new Map();

/**
 * Map of stores
 */
stores.set("default", (params) => new LocalStore((params == null ? "../data.json" : params)))
stores.set("google", (params) => new GoogleStore('cloudsys_bucket'))

/**
 * Store builder
 */
module.exports.CreateStore = function (type = "default", params = null) {
    if (stores.get(type) == null) { type = "default", params = null }
    return (stores.get(type))(params)
}