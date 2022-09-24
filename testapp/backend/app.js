const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { v4: uuidv4 } = require('uuid')
const { LocalStore } = require('./controllers/LocalStore.js');
const { CreateStore } = require('./controllers/StoreBuilder.js');


const hostname = 'localhost';
const port = 3000;



const store = (process.argv[2] == null ? CreateStore() : (process.argv[3] == null ? CreateStore(process.argv[2]) : (CreateStore(process.argv[2], process.argv[3]))));

app.use(
  express.urlencoded({
    extended: true,
    limit: '300mb'
  })
);

app.use(express.json({ limit: '300mb' }));

app.use(function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
  res.setHeader('Access-Control-Allow-Credentials', true);
  next();
});

app.post('/element', (req, res) => {
  req.body.id = uuidv4();
  store.postItem(req.body)

});

app.get('/element/all', (req, res) => {
  res.set('Content-Type', 'application/json');
  res.end(JSON.stringify({ data: store.getAllItems() }));
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});