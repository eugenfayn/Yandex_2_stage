from typing import Union, List
from urllib import response
from matplotlib.pyplot import title
from requests import Session
from fastapi import FastAPI,  Depends, HTTPException, Request, Response
from config import settings
from schemas.units import ShopUnit, ShopUnitImportRequest
from uuid import UUID
import crud
from models import units as models
from db.database import SessionLocal, engine #,get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.project_name,version=settings.project_vers)

#middleware add
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request):
    return request.state.db

@app.post("/imports",response_model=ShopUnit,description="хуй")
def create_unit(unit: ShopUnitImportRequest,db: Session = Depends(get_db)):
    crud.create_unit(db=db, unit=unit)
    
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
  
