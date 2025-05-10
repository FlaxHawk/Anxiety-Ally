from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)
    price: float
    tax: Optional[float] = Field(default=None)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 