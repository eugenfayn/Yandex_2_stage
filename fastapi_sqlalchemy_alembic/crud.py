from fastapi import HTTPException
#from datetime import datetime
from sqlalchemy import null
from sqlalchemy.orm import Session
from uuid import UUID
import models as models
import schema  as schemas

# для запросов. Проверка просто для себя
def get_unit(db):
    return db.query(models.Unit).all()

# В зависимости от присутствия/отсутствия юнита берёт и выкидывает его
def create_unit(db:Session,unit: schemas.ShopUnitImportRequest):
    with db:
        for item in unit.items:
            db_unit = db.query(models.Unit).filter(models.Unit.id==item.id).first()
            db_parent = db.query(models.Unit).filter(models.Unit.id==item.parentId).first()
            if item.parentId and not db_parent:
                # попытка добавить штуку, у которой нет родителя в базе
                raise HTTPException(status_code=404,detail="There's no such parent!!!") 
            if db_parent and db_parent.type==schemas.ShopUnitType.OFFER:
                  #не смог понять,куда правильно эту валидацию кидать
                    raise HTTPException(status_code=404,detail="Offer can't include children!!!") 
            if db_unit:
                update_unit(db,unit,item,db_unit)
            else:
                add_unit(db,unit,item,db_unit)
            
def delete_unit(db,id:UUID):
    db_unit = db.query(models.Unit).filter(models.Unit.id == id).first()
    if not db_unit:
        raise HTTPException(status_code=404,detail="Item not found.") 
    if db_unit.parentId:
       db_parent = db.query(models.Unit).filter(models.Unit.id == db_unit.parentId).first()
       db.delete(db_unit)
       db.commit()
       db_parent.price = new_price(db_parent.children)
       db.commit()
       db.refresh(db_parent)
    else:
        db.delete(db_unit)
        db.commit()
    return {"message": "Delete confirmed!"}

def get_unit_id(db,id:UUID):
    db_unit = db.query(models.Unit).filter(models.Unit.id == id).first()
    if not db_unit:
        raise HTTPException(status_code=404,detail="Item not found.")
    return db_unit

# вспомогательная
def new_price(children):
    count = len(children)
    if count!=0:
        sum_ = 0
        for i in range(count):
            sum_ += children[i].price if children[i].price else 0
        return sum_//count # сделать округление
    else:
        return null

def update_unit(db,unit,item,db_unit):
    db_old_parent = db.query(models.Unit).filter(models.Unit.id==db_unit.parentId).first()
    db_unit.name = item.name
    db_unit.date = unit.updateDate
    db_unit.parentId = item.parentId
    db_new_parent = db.query(models.Unit).filter(models.Unit.id==item.parentId).first()
    if db_unit.type==schemas.ShopUnitType.CATEGORY:
        db.commit()
        db.refresh(db_unit)
        if db_unit.parentId==None or db_old_parent.id == db_new_parent.id: 
            pass
        else: 
            db_old_parent.price = new_price(db_old_parent.children)
            db_new_parent.price = new_price(db_new_parent.children)
            db.commit()
            db.refresh(db_new_parent)
            db.refresh(db_old_parent)
    else:       
            db_unit.price = item.price
            db.commit()
            db.refresh(db_unit)
            if (db_unit.parentId==None):
                pass
            elif (db_old_parent.id == db_new_parent.id):
                db_old_parent.price = new_price(db_old_parent.children)
                db.commit()
                db.refresh(db_new_parent)
                db.refresh(db_old_parent)
            else: 
                db_old_parent.price = new_price(db_old_parent.children)
                db_new_parent.price = new_price(db_new_parent.children)
                db.commit()
                db.refresh(db_new_parent)
                db.refresh(db_old_parent)

def add_unit(db,unit,item,db_unit):
    db_unit = models.Unit(id=item.id,name=item.name,date=unit.updateDate,parentId=item.parentId,type=item.type,price=item.price if item.price else 0)# if item.price else 0)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    if db_unit.parentId:
        db_new_parent = db.query(models.Unit).filter(models.Unit.id==item.parentId).first()
        db_new_parent.price=new_price(db_new_parent.children)
        db.commit()
        db.refresh(db_new_parent)