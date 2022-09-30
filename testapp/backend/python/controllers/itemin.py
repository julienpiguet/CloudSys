from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    title: str
    img: str