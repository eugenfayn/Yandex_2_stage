from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID,ENUM
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,  Enum
#######
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# import os

# engine = create_engine(db_url=os.environ["DATABASE_URL"])
# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     except:
#         db.close()
#######




Base = declarative_base()

class Unit(Base):
    __tablename__ = 'shop_units'
    id = Column(UUID(as_uuid=True),nullable=False,primary_key=True, default=uuid.uuid4)
    name = Column(String(50),nullable=False)
    date = Column(DateTime(),nullable=False)
    parentId = Column(UUID(as_uuid=True),ForeignKey("shop_units.id"))
    type = Column(ENUM('OFFER','CATEGORY',name="unit_type",create_type=False),nullable=False)
    price = Column(Integer(),nullable=True)
    children = relationship("Unit",cascade="all, delete-orphan")





    

    
    