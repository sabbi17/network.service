import logging
from fastapi import FastAPI, HTTPException, Path, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
import models
from models import Base
from database import engine, SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI(
    title="Information of available services (Internet, Phone and TV) in different Locations by phone company",
    description="This rapid application will let you search by zipcode to check which services are available to your location",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Category(Enum):
    INTERNET = "internet"
    CABLE = "cable"
    TV = "tv"
#There is possibility of extending this
#Importing Pydantic and defining a Pydantic model:
class Item(BaseModel):
    id: int = Field(description="Unique integer that specifies this item.")
    zipcode: int = Field(description="Zipcode of the city.")
    city: str = Field(description="Name of the city.")
    price: float = Field(description="Price of the Service in Dollars per month.")
    category: Category = Field(description="Service Provided.")


@app.get("/")
def index(db: Session = Depends(get_db)) -> List[Item]:
    logging.info("Endpoint: /")
    items = db.query(models.Item).all()
    return items


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int, db: Session = Depends(get_db)) -> Item:
    logging.info(f"Endpoint: /items/{item_id}")
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        logging.warning(f"Item with id={item_id} does not exist.")
        raise HTTPException(status_code=404, detail=f"Item with id={item_id} does not exist.")
    return item


@app.get("/items/")
def query_item_by_parameters(
        zipcode: int = None,
        city: str = None,
        price: float = None,
        category: Category = None,
        db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    logging.info("Endpoint: /items/")
    filters = {}
    if zipcode is not None:
        filters["zipcode"] = zipcode
    if city is not None:
        filters["city"] = city
    if price is not None:
        filters["price"] = price
    if category is not None:
        filters["category"] = category.value

    items = db.query(models.Item).filter_by(**filters).all()
    return [item.__dict__ for item in items]

@app.post("/items/")
def add_item(item: Item, db: Session = Depends(get_db)) -> Item:
    logging.info("Endpoint: /items/ [POST]")
    db_item = models.Item(
        id=item.id,
        zipcode=item.zipcode,
        city=item.city,
        price=item.price,
        category=item.category.value
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    # Return a valid dictionary response
    return {"message": "Item created successfully", "item": item.dict()}


@app.put(
    "/update/{item_id}",
    responses={
        404: {"description": "Item not found"},
        400: {"description": "No arguments specified"},
    },
)
def update_item(
        item_id: int,
        item: Item,
        db: Session = Depends(get_db)
) -> Item:
    logging.info(f"Endpoint: /update/{item_id} [PUT]")
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        logging.warning(f"Item with id={item_id} does not exist.")
        raise HTTPException(status_code=404, detail=f"Item with id={item_id} does not exist.")
    db_item.zipcode = item.zipcode
    db_item.city = item.city
    db_item.price = item.price
    db_item.category = item.category.value
    db.commit()
    db.refresh(db_item)
    return item


@app.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    logging.info(f"Endpoint: /delete/{item_id} [DELETE]")
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        logging.warning(f"Item with id={item_id} does not exist.")
        raise HTTPException(status_code=404, detail=f"Item with id={item_id} does not exist.")
    db.delete(db_item)
    db.commit()
    return db_item
