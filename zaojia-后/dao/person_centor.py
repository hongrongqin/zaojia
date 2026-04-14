from sqlalchemy import select, delete
from database.db import session
from models.price_evaluation import FileModel, CostDetailModel, CostReportModel

class PersonCentorDao:
    @classmethod
    async def get_history_by_user_id(cls, user_id: str):
        stmt = select(FileModel).where(FileModel.uploader_user_id == user_id).order_by(FileModel.upload_time.desc())
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_report_by_file_id(cls, file_id: str):
        stmt = select(CostReportModel).where(CostReportModel.file_id == file_id).order_by(CostReportModel.generate_time.desc())
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def delete_history_by_file_id(cls, file_id: str):
        stmt1 = delete(CostDetailModel).where(CostDetailModel.file_id == file_id)
        await session.execute(stmt1)
        
        stmt2 = delete(CostReportModel).where(CostReportModel.file_id == file_id)
        await session.execute(stmt2)

        stmt3 = delete(FileModel).where(FileModel.file_id == file_id)
        await session.execute(stmt3)

        await session.commit()
        return True

    @classmethod
    async def get_file_info_by_id(cls, file_id: str):
        stmt = select(FileModel).where(FileModel.file_id == file_id)
        result = await session.execute(stmt)
        return result.scalars().first()
