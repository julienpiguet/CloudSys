
class Store {

    /**
     * Connection to a remote store service
     * @param {String} url 
     * @returns connection status
     */
    connect(url) {
        return true
    }

    /**
     * Check remote connection status
     * @returns connection status
     */
    isConnected() {
        return true
    }

    /**
     * Post a new Object on the store
     * @typedef {Object} Item
     * @property {string} id
     * @property {string} title
     * @property {string} img
     * @param {Item} item 
     * @returns void
     */
    postItem(item) {
        return
    }

    /**
     * Get an item from the store by his id
     * @typedef {Object} Item
     * @property {string} id
     * @property {string} title
     * @property {string} img
     * @param {String} id 
     * @returns {Item} Item
     */
    getItemById(id) {
        return null
    }

    /**
     * Get all items from the store
     * @typedef {Object} Item
     * @property {string} id
     * @property {string} title
     * @property {string} img
     * @returns {[Item]} Item array
     */
    getAllItems() {
        return []
    }
}

module.exports.Store = Store;