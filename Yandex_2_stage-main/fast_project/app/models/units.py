import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..schemas.units import ShopUnitType
from ..db.database import Base

class Unit(Base):
    __tablename__ = 'shop_units'

    id = sa.Column(UUID(as_uuid=True),nullable=False,primary_key=True, default=uuid.uuid4)
    #id = sa.Column(sa.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = sa.Column(sa.String(50),nullable=False)
    date = sa.Column(sa.DateTime(),nullable=False)
    parentId = sa.Column(UUID(as_uuid=True),sa.ForeignKey("shop_units.id"))
    type = sa.Column(sa.Enum(ShopUnitType),nullable=False)
    price = sa.Column(sa.Integer(),nullable=True)
    children = relationship("Unit",cascade="all, delete-orphan")