from datetime import datetime
from typing import Optional,List
from uuid import UUID
from enum import Enum
from pydantic import Field,BaseModel, validator

class ShopUnitType(str,Enum):
    OFFER="OFFER",
    CATEGORY="CATEGORY"

# isoformat даты
class ShopUnit(BaseModel):
    id: UUID = Field(nullable=False,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Уникальный идентификатор")
    name: str  = Field(nullable=False,description="ИмяКатегории")
    date: datetime = Field(nullable=False,example="2022-05-28T21:12:01.000Z",description="Время последнего обновления элемента")
    parentId: Optional[UUID]= Field(None,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="UUID родительской категории")
    type: ShopUnitType  = Field(nullable=False,description="Тип элемента - категория или товар")
    price: Optional[int]  = Field(None,description="Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null")
    children: Optional[List] = Field(None,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Список всех дочерних товаров\категорий. Для товаров поле равно null")
    
    class Config:
        orm_mode = True

class ShopUnitImport(BaseModel):
    id: UUID = Field(nullable=False,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Уникальный идентификатор")
    name: str = Field(nullable=False,description="ИмяКатегории")
    parentId: Optional[UUID]= None
    type:ShopUnitType = Field(nullable=False,description="Тип элемента - категория или товар")
    price: Optional[int]= Field(None,description="Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null") #int64  

    # если цена null, он даже не зайдет в валидатор
    @validator('price')
    def category_price_is_null(cls,v,values, **kwargs):
        if values['type']==ShopUnitType.CATEGORY:
            raise Error(status_code=400,message="Validation Error")
        return v

    @validator('type',pre=True)
    def offer_price_not_null(cls,v,values, **kwargs):
        return v

class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime
    
    #валидатор даты. Если v=isoformat(), то v.fromisoformat() вернёт дела. иначе выскочит error.
    @validator('updateDate',pre=True)
    def date_format(cls,v):
        try:
            datetime.fromisoformat(v[:-1])
        except:
            raise Error(status_code=400,message="Validation Error")
        return v[:-1]

    # валидатор уникальности id в рамках запроса
    @validator('items',pre=True)
    def all_unique(cls,v):
        id_s = []
        for item in v:
            if item['id'] in id_s:
                raise Error(status_code=400,message="Validation Error")
            else:
                id_s.append(item['id'])
        return v



class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int]=None #int64



class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]



class Error(ValueError):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message