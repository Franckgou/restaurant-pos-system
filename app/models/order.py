from app.core.database import Base, TimestampMixin
from sqlalchemy import  ForeignKey,Numeric, Column, Float, DateTime, String, Integer, Boolean
from enum import Enum as PyEnum
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

class OrderTrack(PyEnum):
    cooking = "cooking"
    ready = "ready"
    served = "served"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True, nullable = False)
    total_amount = Column(Numeric(10,2), nullable = False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable = False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable = False)
    served_at = Column(DateTime, nullable = False)
    order_id = Column(String, nullable = False, unique = True)


    employee = relationship("Employee", back_populates = "orders")

    table = relationship("Table", back_populates= "orders")

    order_items = relationship("Order_Item", back_populates= "order", cascade = "all, delete-orphan")