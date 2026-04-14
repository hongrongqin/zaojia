from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from schemas.management_maintenance import CostPeopleResponse, CostPeopleCreate
from services.management_maintenance import CostPeopleService

router = APIRouter()

@router.get("/cost-people", response_model=List[CostPeopleResponse], summary="获取各市最新造价信息")
async def get_latest_city_prices(db: AsyncSession = Depends(get_db)):
    """
    获取每个城市的最新价格，用于前端展示。城市去重，保留最新的记录。
    """
    return await CostPeopleService.get_latest_city_prices(db)

@router.post("/cost-people", response_model=CostPeopleResponse, summary="修改当前城市价格及新增城市")
async def add_or_update_city_price(data: CostPeopleCreate, db: AsyncSession = Depends(get_db)):
    """
    前端修改价格或新增没有的城市价格
    """
    return await CostPeopleService.create_cost_people(db, data)

