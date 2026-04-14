from pydantic import BaseModel

from typing import Optional



class CostDetailUpdateReq(BaseModel):

    id: int

    item_name: Optional[str] = None

    function_category: Optional[str] = None

    us: Optional[float] = None

    comment: Optional[str] = None
    repair_type: Optional[str] = None

class CalculatePriceReq(BaseModel):
    file_id: str
    CF: float
    PDR: float
    AT: float
    QR: float
    XC: float
    HM: float
    city: str

class EvaluateConfigUpdateReq(BaseModel):
    key: str
    value: float
    annotation: Optional[str] = None


