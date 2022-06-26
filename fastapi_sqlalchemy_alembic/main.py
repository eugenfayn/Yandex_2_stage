from typing import List
import uvicorn
from fastapi import FastAPI, Request, Depends
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from sqlalchemy.orm import Session
from models.models import Unit
from schemas.schema import ShopUnitImport,ShopUnit, ShopUnitImportRequest
from dotenv import load_dotenv
import utils.crud as crud
from uuid import UUID
from config import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI(title=settings.project_name,version=settings.project_vers)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.post("/unitsss/",response_model=ShopUnit)  #Schema
def create_user(user: ShopUnit): #Schema
    db_user = Unit(
        id=user.id, name=user.name, date=user.date,parentId=user.parentId,
        type=user.type,price=user.price,children=user.children
    )
    print(type(db.session))
    #db.session.add(db_user)
    db.session.commit()
    return db_user

@app.post("/imports",response_model=ShopUnitImport,description="дескрипшен")
def create_unit(unit: ShopUnitImportRequest):
        crud.create_unit(db.session, unit)
    
@app.get("/unit/", response_model=List[ShopUnit])
def read_units():
        units = crud.get_unit(db.session)
        return units

@app.get("/nodes/{id}",response_model=ShopUnit)
def get_unit(id: UUID):
        return crud.get_unit_id(db.session,id)


@app.delete("/delete/{id}")#,response_model=ShopUnit)
def delete_units(id: UUID):
        return crud.delete_unit(db.session,id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)