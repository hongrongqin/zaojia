from pydantic import BaseModel
from datetime import datetime

class ProjectFileResp(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    upload_time: datetime
    
    class Config:
        orm_mode = True
