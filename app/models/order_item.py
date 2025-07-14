from sqlalchemy import Numeric, ForeignKey,DateTime, String,Float, Column, Integer, Boolean  # from enum import Enum as PYEnum
from app.core.database import Base, TimestampMixin
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

class Order_Item(Base, TimestampMixin):
    __tablename__ = "order_items"
    
    id = Column(Integer, nullable = False, primary_key= True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable = False)
    menu_item_id = Column(Integer, ForeignKey('menu.id'), nullable = False)
    quantity = Column(Integer, nullable = False, default = 1)
    item_price = Column(Numeric(10, 2), nullable = False)


    
    order = relationship("Order", back_populates = "order_items")

    menu_item = relationship("Menu", back_populates= "order_items")
