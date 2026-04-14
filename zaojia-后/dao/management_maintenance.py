from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.management_maintenance import CostPeople
from schemas.management_maintenance import CostPeopleCreate

class CostPeopleDAO:
    @staticmethod
    async def get_latest_city_prices(db: AsyncSession):
        # 获取每个城市最新的数据
        # 使用子查询：先查出每个 city 对应的最大 create_time
        subq = select(
            CostPeople.city, 
            func.max(CostPeople.create_time).label("max_time")
        ).group_by(CostPeople.city).subquery()

        # 将子查询和原表 join，获取最新条目的 price 等信息
        query = select(CostPeople).join(
            subq,
            (CostPeople.city == subq.c.city) & (CostPeople.create_time == subq.c.max_time)
        )
        
        result = await db.execute(query)
        # 注意: 如果有多个相同最大时间的同城记录，此方法可能会都扫出来，在实际业务中通常够用
        return result.scalars().all()

    @staticmethod
    async def create_cost_people(db: AsyncSession, obj_in: CostPeopleCreate):
        db_obj = CostPeople(
            city=obj_in.city,
            price=obj_in.price
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
