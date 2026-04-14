from sqlalchemy.ext.asyncio import AsyncSession
from dao.management_maintenance import CostPeopleDAO
from schemas.management_maintenance import CostPeopleCreate

class CostPeopleService:
    @staticmethod
    async def get_latest_city_prices(db: AsyncSession):
        return await CostPeopleDAO.get_latest_city_prices(db)

    @staticmethod
    async def create_cost_people(db: AsyncSession, obj_in: CostPeopleCreate):
        return await CostPeopleDAO.create_cost_people(db, obj_in)
