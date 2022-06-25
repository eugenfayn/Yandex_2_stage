#from numpy import int64, integer
from datetime import datetime
from turtle import update
from typing import Optional,List
from uuid import UUID
from enum import Enum
from pydantic import Field,BaseModel


class ShopUnitType(str,Enum):
    OFFER="OFFER",
    CATEGORY="CATEGORY"

class ShopUnit(BaseModel):
    id: UUID = Field(nullable=False,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Уникальный идентификатор")
    name: str  = Field(nullable=False,description="ИмяКатегории")
    date: datetime  = Field(nullable=False,example="2022-05-28T21:12:01.000Z",description="Время последнего обновления элемента")
    parentId: Optional[UUID]= Field(None,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="UUID родительской категории")
    type: ShopUnitType  = Field(nullable=False,description="Тип элемента - категория или товар")
    price: Optional[int]  = Field(None,description="Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null")
    children: Optional[List] = Field(None,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Список всех дочерних товаров\категорий. Для товаров поле равно null")

    class Config:
        orm_mode = True

class ShopUnitImport(BaseModel):
    id: UUID = Field(nullable=False,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="Уникальный идентификатор")
    name: str = Field(nullable=False,description="ИмяКатегории")
    parentId: Optional[UUID]= Field(None,example="3fa85f64-5717-4562-b3fc-2c963f66a333",description="UUID родительской категории")
    type:ShopUnitType = Field(nullable=False,description="Тип элемента - категория или товар")
    price: Optional[int]= Field(None,description="Целое число, для категории - это средняя цена всех дочерних товаров(включая товары подкатегорий). Если цена является не целым числом, округляется в меньшую сторону до целого числа. Если категория не содержит товаров цена равна null") #int64  

class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime 

class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int]=None #int64

class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]

class Error(BaseModel):
    code: int
    message: str
