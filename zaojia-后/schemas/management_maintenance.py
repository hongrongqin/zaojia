from pydantic import BaseModel
from typing import Optional

class CostPeopleBase(BaseModel):
    city: str
    price: float

class CostPeopleCreate(CostPeopleBase):
    pass

class CostPeopleResponse(CostPeopleBase):
    class Config:
        from_attributes = True
