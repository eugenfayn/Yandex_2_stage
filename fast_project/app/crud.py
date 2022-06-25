from http.client import HTTPException
from sqlalchemy import null
from sqlalchemy.orm import Session
from uuid import UUID
from models import units as models
from schemas import units as schemas

# для запросов
def get_unit(db: Session):
    return db.query(models.Unit).all()

# выдаёт ошибку
# sqlalchemy.orm.exc.UnmappedInstanceError: Class 'builtins.int' is not mapped
def create_unit(db:Session,unit: schemas.ShopUnitImportRequest):
    for item in unit.items:
        db_unit = db.query(models.Unit).filter(models.Unit.id==item.id).first()
        if db_unit:
            db_old_parent = db.query(models.Unit).filter(models.Unit.id==db_unit.parentId).first()
            db_unit.name = item.name
            db_unit.date = unit.updateDate
            db_unit.parentId = item.parentId
            db_new_parent = db.query(models.Unit).filter(models.Unit.id==item.parentId).first()
            # Если меняем type у unit, выводим еррор 400
            # При переносе подкатегории в другую категорию мы должны изменить цену у старой и новой родительской категории
            # Если переносится ТОВАР в другую категорию, поступаем аналогичным образом
            # Если родительская категория отсутствует или не изменяется, цена может измениться только в случае, если это товар, потому что у категорий это null
            if db_unit.type=="CATEGORY":
                if (db_old_parent.id == db_new_parent.id) or (db_unit.parentId==None):
                    pass
                else: 
                    db_old_parent.price = new_price(db_old_parent.children)
                    db_new_parent.price = new_price(db_new_parent.children)
                    db.commit()
                    db.refresh(db_unit)
                    db.refresh(db_new_parent)
                    db.refresh(db_old_parent)
            else:       
                db_unit.price = item.price
                if (db_old_parent.id == db_new_parent.id) or (db_unit.parentId==None):
                    db_old_parent.price = new_price(db_old_parent.children)
                    db.commit()
                    db.refresh(db_unit)
                    db.refresh(db_new_parent)
                    db.refresh(db_old_parent)
                else: 
                    db_old_parent.price = new_price(db_old_parent.children)
                    db_new_parent.price = new_price(db_new_parent.children)
                    db.commit()
                    db.refresh(db_unit)
                    db.refresh(db_new_parent)
                    db.refresh(db_old_parent)
        else:
            db_unit = models.Unit(id=item.id,name=item.name,date=unit.updateDate,parentId=item.parentId,type=item.type,price=item.price)# if item.price else 0)
            db.add(db_unit)
            if db_unit.parentId:
                db_new_parent = db.query(models.Unit).filter(models.Unit.id==item.parentId).first()
                db_new_parent.price=new_price(db_new_parent.children)
                db.commit()
                db.refresh(db_new_parent)
                db.refresh(db_unit)
            db.commit()
            db.refresh(db_unit)
    return db_unit

def delete_unit(db:Session,id:UUID):
    db_unit = db.query(models.Unit).filter(models.Unit.id == id).first()
    if db_unit.parentId:
        db_parent = db.query(models.Unit).filter(models.Unit.id == db_unit.parentId).first()
    if not db_unit:
        raise HTTPException(status_code=404,detail="Item not found.") # HTTPException() takes no keyword arguments
    db.delete(db_unit)
    db_parent.price = new_price(db_parent.children)
    db.commit()
    db.refresh(db_parent)
    return {"message": "Delete confirmed!"}

def get_unit_id(db:Session,id:UUID):
    db_unit = db.query(models.Unit).filter(models.Unit.id == id).first()
    if not db_unit:
        raise HTTPException(statis_code=404,detail="Item not found.")
    return db_unit

# вспомогательная
def new_price(children):

    count = len(children)
    if count!=0:
        summa = 0
        for i in range(count):
            summa += children[i].price
        return summa//count # сделать округление
    else:
        return 0 #null

def validation_import(item):
    return 