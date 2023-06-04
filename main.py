
from pydantic import BaseModel, Field
from enum import Enum
from fastapi import FastAPI, HTTPException, Path, Query, Depends
import models
from database import engine,  SessionLocal
from sqlalchemy.orm import Session
from typing import List,Dict



# API a title and additional metadata such as a description, version number.

app = FastAPI(
    title="Information of avaliable services(Internet, Phone and TV) in different Locations by phone company",
    description="This rapid application will let you search by zipcode to check which services are avaliable to your location",
    version="0.1.0",
)

# Created Db Table if not auto created.
models.Base.metadata.create_all(bind=engine)


#opening and closing the Db.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Docstrings of classes will be reflected  in the 'Schemas' section in the API documentation.
class Category(Enum):
    """Category of an item"""

    INTERNET = "internet"
    CABLE = "cable"
    TV = "tv"


# Adding metadata to attributes using the Field class.
# This information will also be shown in the auto-generated documentation.
class Item(BaseModel):

    id: int = Field(description="Unique integer that specifies this item.")
    zipcode: int = Field(description="Zipcode of the city.")
    city: str = Field(description="Name of the city.")
    price: float = Field(description="Price of the Service in Dollars per month.")
    category: Category = Field(description="Service Provided.")

#I intentionally commented out the manuall entry of DB would need to delete it after the review.

# items = {
#     0: Item(id=0,zipcode=83716,city="Boise", price=80,category=Category.TV),
#     1: Item(id=1,zipcode=83715,city="Meridian", price=50.99, category=Category.INTERNET),
#     2: Item(id=2,zipcode=83712,city="Nampa", price=85.99, category=Category.CABLE),
# }

# Adding Manually
# @app.get("/")
# def index() -> dict[str, dict[int, Item]]:
#     return {"items": items}

@app.get("/")
def index(db: Session = Depends(get_db)) -> List[Item]:
    items = db.query(models.service_app).all()
    return items

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    return items[item_id]

#FastAPI will returns an error message when arguments are incorrect.
Selection = dict[
    str, int | str | float | Category | None
]  # dictionary containing the user's query arguments


@app.get("/items/")
def query_item_by_parameters(
    zipcode: int | None = None,
    city: str | None = None,
    price: float | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:


    def check_item(item: Item):
        """Check if the item matches the query arguments from the outer scope."""
        return all(
            (
                zipcode is None or item.zipcode == zipcode,
		        city is None or item.city == city,
                price is None or item.price == price,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": { "zipcode": zipcode, "city": city, "price": price, "category": category},
        "selection": selection,
    }

#Manually Adding of Items is commented out for reference.

@app.post("/")
# def add_item(item: Item) -> dict[str, Item]:
#     if item.id in items:
#         HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")
#
#     items[item.id] = item
#     return {"added": item}

def add_item(item: Item, db: Session = Depends(get_db)) -> dict[str, Item]:
    db_item = models.Item(
        id=item.id,
        zipcode=item.zipcode,
        city=item.city,
        price=item.price,
        category=item.category.value,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"added": item}

# The 'responses' keyword allows you to specify which responses a user can expect from this endpoint.
@app.put(
    "/update/{item_id}",
    responses={
        404: {"description": "Item not found"},
        400: {"description": "No arguments specified"},
    },
)
# The Query and Path classes also allow us to add documentation to query and path parameters.
def update(
    item_id: int = Path(
        title="Item ID", description="Unique integer that specifies an item.", ge=0
    ),

    zipcode: int
    | None = Query(
        title="Zipcode",
        description="Enter a new zipcode.",
        default=None,
        ge=0,
    ),
    city: str
    | None = Query(
        title="City",
        description="Please provide the city name for this Zipcode.",
        default=None,
        min_length=1,
        max_length=8,
    ),
    price: float
    | None = Query(
        title="Price",
        description="New price for this City per month",
        default=None,
        gt=0.0,
    ),

):

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    if all(info is None for info in (zipcode, city, price)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]
    if zipcode is not None:
        item.zipcode = zipcode
    if city is not None:
        item.city = city
    if price is not None:
        item.price = price

    return {"updated": item}


@app.delete("/delete/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )

    item = items.pop(item_id)
    return {"deleted": item}
