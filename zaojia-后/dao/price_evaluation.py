from sqlalchemy import select, update
from dao.base import BaseDao
from database.db import session
from models.price_evaluation import FileModel, CostDetailModel

class FileDao(BaseDao):

    @classmethod
    async def create_file(cls, obj_dict: dict):
        new_file = FileModel(**obj_dict)
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file) # 确保使用异步方式刷新，而不是在后续使用属性时触发同步过期加载报错
        return new_file


class CostDetailDao(BaseDao):

    @classmethod
    async def get_by_file_id(cls, file_id: str):
        stmt = select(CostDetailModel).where(CostDetailModel.file_id == file_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update_detail(cls, item_id: int, update_data: dict):
        stmt = update(CostDetailModel).where(CostDetailModel.id == item_id).values(**update_data)
        await session.execute(stmt)
        await session.commit()
        return True


from models.price_evaluation import CostReportModel, EvaluateConfigModel
from models.management_maintenance import CostPeople

class CostReportDao(BaseDao):
    @classmethod
    async def create_report(cls, report_data: dict) -> CostReportModel:
        new_report = CostReportModel(**report_data)
        session.add(new_report)
        await session.commit()
        await session.refresh(new_report)
        return new_report

    @classmethod
    async def get_by_file_id(cls, file_id: str):
        stmt = select(CostReportModel).where(CostReportModel.file_id == file_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def update_report(cls, report_id: str, report_data: dict) -> CostReportModel:
        stmt = update(CostReportModel).where(CostReportModel.report_id == report_id).values(**report_data)
        await session.execute(stmt)
        await session.commit()
        stmt_sel = select(CostReportModel).where(CostReportModel.report_id == report_id)
        result = await session.execute(stmt_sel)
        return result.scalars().first()
        
class EvaluateConfigDao(BaseDao):
    @classmethod
    async def get_all_config(cls):
        stmt = select(EvaluateConfigModel)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update_config(cls, key: str, value: float):
        stmt = update(EvaluateConfigModel).where(EvaluateConfigModel.key == key).values(value=value)
        await session.execute(stmt)
        await session.commit()
        return True

    @classmethod
    async def update_config_dict(cls, key: str, update_data: dict):
        stmt = update(EvaluateConfigModel).where(EvaluateConfigModel.key == key).values(**update_data)
        await session.execute(stmt)
        await session.commit()
        return True

class CostPeopleDao(BaseDao):
    @classmethod
    async def get_latest_cost_by_city(cls, city: str):
        stmt = select(CostPeople).where(CostPeople.city == city).order_by(CostPeople.create_time.desc()).limit(1)
        result = await session.execute(stmt)
        return result.scalars().first()

class FileDaoExtended(FileDao):
    @classmethod
    async def get_file_by_id(cls, file_id: str):
        stmt = select(FileModel).where(FileModel.file_id == file_id)
        result = await session.execute(stmt)
        return result.scalars().first()


