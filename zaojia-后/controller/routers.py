from fastapi import APIRouter
from core.config import settings
from controller.v1.user import router as user_router
from controller.v1.price_evaluation import router as price_eval_router
from controller.v1.management_maintenance import router as current_maint_router
from controller.v1.person_centor import router as person_centor_router


v1 = APIRouter(prefix=settings.FASTAPI_API_PREFIX)
v1.include_router(user_router, prefix='/user', tags=["用户"])
v1.include_router(price_eval_router, prefix='/price_evaluation', tags=["价格评估"])
v1.include_router(current_maint_router, prefix='/management_maintenance', tags=["管理维护"])
v1.include_router(person_centor_router, prefix='/person_center', tags=["个人中心"])


