from fastapi import FastAPI, status, HTTPException
import requests
import json
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models

app = FastAPI(title="My First API",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc"
              )

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float    
    on_offer: Optional[bool] = None

    class Config:
        orm_mode = True
        

db=SessionLocal()


@app.get("/items", response_model= List[Item], status_code= status.HTTP_200_OK)
async def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_an_item(item: Item):
    new_item = models.Item(name=item.name, description=item.description, price=item.price, on_offer=item.on_offer)
    db_item = db.query(models.Item).filter(models.Item.name == new_item.name).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item    


@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def update_an_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer
    
    db.commit()
    db.refresh(item_to_update)
    return item_to_update


@app.delete("/items/{item_id}")
async def delete_an_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    db.delete(item_to_delete)
    db.commit()
    return {"message": "Item deleted successfully"}


# create a proxy api endpoint to redirect to external api and return the response
@app.get("/proxy")
async def proxy(ext_api: str, ext_api_key: str = None):    
    headers = {"Authorization": f"Bearer {ext_api_key}"}
    response = requests.get(ext_api, headers=headers)
    return response.json()

