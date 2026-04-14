from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from common.response.schema import responseBase
from services.price_evaluation import FileService, CostDetailService
from schemas.jwt import UserInfo
from services.jwt import JwtService
from schemas.price_evaluation import CostDetailUpdateReq
from schemas.price_evaluation import CalculatePriceReq, EvaluateConfigUpdateReq
from services.price_evaluation import PriceEvaluationService
from common.response.code_base import BaseStatus

router = APIRouter()


@router.post("/upload", summary="上传文件及解析")
async def upload_file(
    file: UploadFile = File(..., description="要上传解析的文件"),
    uploader_user_id: str = Form(..., description="上传该文件的用户ID")

):
    try:
        result = await FileService.upload_and_parse_file(file, uploader_user_id)
        return await responseBase.success(data=result, msg="文件上传并解析成功")
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"处理文件异常: {str(e)}")



@router.get("/cost_detail/list", summary="根据文件ID获取报告详情列表")
async def get_cost_details(file_id: str = Query(..., description="文件ID")):
    try:
        result = await CostDetailService.get_details_by_file_id(file_id)
        return await responseBase.success(data=result)
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"查询失败: {str(e)}")



@router.put("/cost_detail/update", summary="修改报告详情某条数据")
async def update_cost_detail(req: CostDetailUpdateReq):
    try:
        await CostDetailService.update_detail(req)
        return await responseBase.success(msg="修改成功")
    except Exception as e:

        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"修改失败: {str(e)}")



@router.post('/calculate', summary='计算价格')
async def calculate_price(req: CalculatePriceReq):
    try:
        result = await PriceEvaluationService.calculate_price(req)
        return await responseBase.success(data=result, msg='计算成功')
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=str(e))

@router.get('/evaluate_config/default', summary='获取默认评估配置')
async def get_evaluate_config():
    try:
        result = await PriceEvaluationService.get_evaluate_config()
        return await responseBase.success(data=result, msg='获取默认评估配置成功')
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=str(e))



@router.put('/evaluate_config/update', summary='修改默认评估配置')
async def update_evaluate_config(req: EvaluateConfigUpdateReq):
    try:
        await PriceEvaluationService.update_evaluate_config(req)
        return await responseBase.success(msg='修改默认评估配置成功')
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=str(e))
