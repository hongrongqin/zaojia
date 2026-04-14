from datetime import datetime

from sqlalchemy import Column, String
from models import Base


class UserModel(Base):
    __tablename__ = 'user'

    uid = Column(String(255), primary_key=True, unique=True, nullable=False, comment='用户id')
    username = Column(String(64), nullable=False, comment='用户名')
    password = Column(String(64), nullable=False, comment='密码')
    role_type = Column(String(64), default="普通用户", nullable=True, comment='身份')
    phone = Column(String(64), nullable=True, comment='手机号')
