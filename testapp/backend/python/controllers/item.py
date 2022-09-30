from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str
    title: str
    img: str