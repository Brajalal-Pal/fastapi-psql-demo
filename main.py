from fastapi import FastAPI, status
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

@app.get("/items/{item_id}")
async def get_an_item(item_id: int):
    pass


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_an_item(item: Item):
    new_item = models.Item(name=item.name, description=item.description, price=item.price, on_offer=item.on_offer)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item    

@app.put("/items/{item_id}")
async def update_an_item(item_id: int):
    pass

@app.delete("/items/{item_id}")
async def delete_an_item(item_id: int):
    pass




