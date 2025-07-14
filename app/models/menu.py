from app.core.database import Base, TimestampMixin
from sqlalchemy import ForeignKey ,Numeric, Column, Integer, Boolean, String, DateTime
from enum import Enum as PyEnum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

class Categories(PyEnum):
    appetizer = "appetizer"
    entree = "entree"
    dessert = "dessert"
    drink = "drink"

class Menu(Base, TimestampMixin):
    __tablename__ = "menu"

    id = Column(Integer, nullable = False, primary_key = True)
    availability = Column(Boolean, default = True, nullable = False)
    item_name = Column(String(30), nullable = False)
    description = Column(String(200), nullable = True)
    price = Column(Numeric(10, 2), nullable = False)
    categories = Column(SQLEnum(Categories), nullable = False)
    
    order_items = relationship("Order_Item", back_populates= "menu_item")
