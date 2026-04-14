from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database.db import Base

class CostPeople(Base):
    __tablename__ = "cost_people"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city = Column(String(100), nullable=True)
    price = Column(Float, nullable=True)
    create_time = Column(DateTime, default=func.now(), nullable=False)
