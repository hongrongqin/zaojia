from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    created_at = Column(DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    is_delete = Column(Boolean, default=False, comment='是否删除')
