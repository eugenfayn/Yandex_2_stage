from typing import Union, List
from urllib import response
from matplotlib.pyplot import title
from requests import Session
from fastapi import FastAPI,  Depends
from pydantic import BaseModel
from config import settings
from schemas.units import ShopUnit, ShopUnitImport, ShopUnitImportRequest, Error
from uuid import UUID

import crud
from models import units as models
from schemas import units as schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.project_name,version=settings.project_vers)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/imports",response_model=ShopUnit)
def create_unit(unit: ShopUnitImportRequest,db: Session = Depends(get_db)):
     return crud.create_unit(db=db, unit=unit)
    
@app.get("/unit/", response_model=List[ShopUnit])
def read_units(db: Session = Depends(get_db)):
    units = crud.get_unit(db)
    return units

@app.get("/nodes/{id}",response_model=ShopUnit)
def get_unit(id: UUID, db: Session = Depends(get_db)):
    return crud.get_unit_id(db,id)


@app.delete("/delete/{id}")#,response_model=ShopUnit)
def delete_units(id: UUID, db: Session = Depends(get_db)):
    return crud.delete_unit(db,id)
  











# class Item2(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.get("/")
# def read_root():
#     return {"Hello": "Zalupadddd"}

# # @app.get("/items/{item_id}")
# # def read_item(item_id: int, q: Union[str, None] = None):
# #     return {"item_id": item_id, "q": q}

# @app.put("/shop/{shopunit_id}")
# def update_shopunit(shopunit_id:int,shopunit: ShopUnit):
#     return {"unit_name":shopunit.name}

# @app.post("/imports")
# def update_shopunit(shopunit:ShopUnitImportRequest):
#     # try:
#         return shopunit
#     # except:
#     #      raise HTTPException(status_code=404, detail="Item not found")

# # @app.delete("/delete/{id}")
# # def delete_shopunit(id:UUID)
