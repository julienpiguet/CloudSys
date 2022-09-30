# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
#from controllers import Store, Item, get_store
from controllers.item import Item
from controllers.itemin import ItemIn
from controllers.store_builder import get_store
import uuid
import configparser

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = configparser.ConfigParser()
config.read('config.ini')
storetype = config['DEFAULT']['StoreType']


store = get_store(storetype, config[storetype]['arg'] if config.has_option(storetype, 'arg') else None)

@app.get("/element/all")
async def get_all_element():
    return JSONResponse(content=jsonable_encoder(store.getAllItems()))

@app.post("/element", status_code=201)
async def add_element(item: ItemIn):
    store.postItem(Item(id=str(uuid.uuid4()), title=item.title, img=item.img))
    return item