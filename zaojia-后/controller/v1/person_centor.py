from fastapi import APIRouter, Query
from common.response.schema import responseBase
from common.response.code_base import BaseStatus
from services.person_centor import PersonCentorService

router = APIRouter()

@router.get("/history", summary="获取用户历史评估记录")
async def get_user_history(user_id: str = Query(..., description="用户ID")):
    try:
        data = await PersonCentorService.get_user_history(user_id)
        return await responseBase.success(data=data, msg="获取历史记录成功")
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"获取失败: {str(e)}")

@router.delete("/history", summary="删除用户历史评估记录")
async def delete_user_history(file_id: str = Query(..., description="文件ID")):
    try:
        await PersonCentorService.delete_history_by_file_id(file_id)
        return await responseBase.success(msg="删除成功")
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"删除失败: {str(e)}")

@router.get("/report", summary="获取造价报告详情")
async def get_cost_report(file_id: str = Query(..., description="文件ID")):
    try:
        data = await PersonCentorService.get_report_by_file_id(file_id)
        if not data:
            return await responseBase.fail(status=BaseStatus.CLIENT_ERROR, msg="报告未找到")
        return await responseBase.success(data=data, msg="获取报告成功")
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"获取失败: {str(e)}")

@router.get("/file_info", summary="根据文件ID获取文件详细信息")
async def get_file_info(file_id: str = Query(..., description="文件ID")):
    try:
        data = await PersonCentorService.get_file_info_by_id(file_id)
        if not data:
            return await responseBase.fail(status=BaseStatus.CLIENT_ERROR, msg="文件未找到")
        return await responseBase.success(data=data, msg="获取文件信息成功")
    except Exception as e:
        return await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=f"获取失败: {str(e)}")
    
