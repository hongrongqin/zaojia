from sqlalchemy import Column, String, Text, DateTime, Integer, Float
from sqlalchemy.sql import func
from models import Base

class FileModel(Base):

    __tablename__ = 'project_file'

    file_id = Column(String(255), primary_key=True, comment='文档ID，主键')
    file_name = Column(String(255), nullable=False, comment='文档名称')
    file_content = Column(Text, nullable=True, comment='文档内容')
    file_type = Column(String(20), nullable=False, comment='文档类型（如：pdf, docx, txt）')
    file_storage_path = Column(String(500), nullable=False, comment='文档存储路径')
    uploader_user_id = Column(String(255), nullable=False, comment='上传人ID')
    upload_time = Column(DateTime, server_default=func.now(), nullable=False, comment='上传时间')


class CostDetailModel(Base):

    __tablename__ = 'report_detail'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='明细ID，主键')
    report_id = Column(String(255), nullable=True, comment='所属报告ID，关联cost_report表')
    file_id = Column(String(255), nullable=True, comment='所属文件ID')
    item_name = Column(String(255), nullable=True, comment='功能点计数项名称')
    function_category = Column(String(50), nullable=True, comment='功能点类别（如：EI, EO, EQ, ILF, EIF）')
    ufp = Column(Integer, nullable=True, comment='UFP')
    reuse_degree = Column(String(30), nullable=True, comment='重用程度（高）')
    us = Column(Float, nullable=True, comment='US（调整因子或系数）')
    comment = Column(Text, nullable=True, comment='备注')
    repair_type = Column(String(20), nullable=True, comment='修改类型')

class CostReportModel(Base):

    __tablename__ = 'cost_report'

    report_id = Column(String(255), primary_key=True)
    file_id = Column(String(255))
    file_name = Column(String(200))
    generator_user_id = Column(String(255))
    total_price = Column(Float)
    unit_price = Column(Float)
    ei_total = Column(Integer)
    eo_total = Column(Integer)
    eq_total = Column(Integer)
    ilf_total = Column(Integer)
    eif_total = Column(Integer)
    adjust_before_us_total = Column(Float)
    adjust_after_us_total = Column(Float)
    cf = Column(Float)
    pdr = Column(Float)
    at = Column(Float)
    qr = Column(Float)
    xc = Column(Float)
    hm = Column(Float)
    city_price = Column(String(100))
    generate_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

class EvaluateConfigModel(Base):
    __tablename__ = 'evaluate_config'
    key = Column(String(255), primary_key=True)
    value = Column(Float)
    annotation = Column(String(255), nullable=True, comment='注释')


