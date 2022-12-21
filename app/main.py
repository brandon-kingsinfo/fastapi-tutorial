from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from enum import Enum
import uvicorn
from typing import Optional
from input_models import Item
from routers.files import urls as files
from routers.auth import urls as auth

def test_main():
    print('test main...')


app = FastAPI()

app.mount("/static",StaticFiles(directory="static"), name="static")

app.include_router(
    auth.router,
    prefix="/auth",
)

app.include_router(
    files.router,
    prefix="/files",
)

# basic routes


@app.get("/")
async def root():
    return {"message": "sample get route to root page"}


@app.post("/")
async def root():
    return {"message": "sample post route to root page"}


@app.get("/deprecated", description="this route is deprecated", deprecated=True)
async def deprecated():
    return {"message": "this route is deprecated, dont' use it!"}


@app.post("/echo")
async def echo(cmd:str = Body(..., embed=True)):
    return cmd

# path parameters
fake_items = [
    {"id": 1, "name": "iPhone"},
    {"id": 2, "name": "iPad"},
    {"id": 3, "name": "iToilet"},
    {"id": 4, "name": "iPod"},
    {"id": 5, "name": "iJoke"},
    {"id": 6, "name": "iLamp"},
    {"id": 7, "name": "iOven"}
]


@app.get("/items")
async def get_items():
    return fake_items


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# specific route must go before dynamic route!
# /users/me must be above /users/{user_id}, sometimes order matters


@app.get("/users/me")
async def get_current_user():
    return {"message": "getting current user"}


@app.get("/users/{user_id}")
async def get_current_user(user_id: str):
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run(app)

# dealing with Enum
# swagger will list available values as fruits, veggie, and dairy


class FoodEnum(str, Enum):
    Fruits = "fruits"
    Vaggie = "veggie"
    Dairy = "dairy"


@app.get("/food/{food_name}")
async def get_food(food_name: FoodEnum):
    return {"food_name": food_name}

# query parameters
# query parameters won't appear in route decorator
# http://localhost:8000/fake_items?skip=5&limit=10


@app.get("/fake_items")
async def get_fake_items(skip: int = 0, limit: int = 7):
    return fake_items[skip:skip+limit]

# Optional query parameter and type conversion
# q is an optional param, and update is a bool
# fastapi will convert 1, on, true, etc. to boolean True
# while 0 off, false, etc will be converted to boolean False


@app.get("/fake_items/{item_id}")
async def get_fake_items(item_id: int, q: Optional[str] = None, update: bool = False):
    item = {"item_id": item_id}
    if q:
        return {"q": q}

    if update:
        item.update({"desc": "lorem ipsum"})
        return item

    for i in fake_items:
        if i["id"] == item_id:
            return i
    return JSONResponse(status_code=404, content={"message": "item not found"})

# request body


@app.post("/items")
async def create_item(item: Item):
    '''anything that is based on BaseModel has a dict() method to convert itself into a dictionary'''
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
