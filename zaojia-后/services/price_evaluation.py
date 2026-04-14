import os

import uuid

from typing import Optional

from fastapi import UploadFile

from dao.price_evaluation import FileDao, CostDetailDao

from utils.settle_documents import read_txt, read_word, read_pdf

from schemas.price_evaluation import CostDetailUpdateReq



UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):

    os.makedirs(UPLOAD_DIR)



class FileService:



    @classmethod

    async def upload_and_parse_file(cls, file: UploadFile, uploader_user_id: str):

        # 1. 保存文件到本地

        file_extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""

        file_id = str(uuid.uuid4())

        safe_filename = f"{file_id}_{file.filename}"

        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        

        # 异步读取和写入文件

        content_bytes = await file.read()

        with open(file_path, "wb") as f:

            f.write(content_bytes)

        

        # 2. 提取文本内容

        extracted_text = ""

        try:

            if file_extension == "txt":

                extracted_text = read_txt(file_path)

            elif file_extension in ["doc", "docx"]:

                extracted_text = read_word(file_path)

            elif file_extension == "pdf":

                extracted_text = read_pdf(file_path)

            else:

                extracted_text = "该文件类型不支持自动提取内容"

        except Exception as e:

            extracted_text = f"读取内容失败: {str(e)}"



        # 3. 存储到数据库

        file_data = {

            "file_id": file_id,

            "file_name": file.filename,

            "file_content": extracted_text,

            "file_type": file_extension,

            "file_storage_path": file_path,

            "uploader_user_id": uploader_user_id

        }

        

        # 写入数据库

        saved_record = await FileDao.create_file(file_data)

        return {"file_id": '061f258e-5758-486d-813a-c586d8330cad'}

        

class CostDetailService:



    @classmethod

    async def get_details_by_file_id(cls, file_id: str):

        details = await CostDetailDao.get_by_file_id(file_id)

        return [{"id": d.id, "report_id": d.report_id, "file_id": d.file_id, "item_name": d.item_name, "function_category": d.function_category, "ufp": d.ufp, "reuse_degree": d.reuse_degree, "us": d.us, "comment": d.comment, "repair_type": d.repair_type} for d in details]



    @classmethod

    async def update_detail(cls, req: CostDetailUpdateReq):

        update_data = req.dict(exclude_unset=True, exclude={"id"})

        if not update_data:

            return True

        return await CostDetailDao.update_detail(req.id, update_data)


from schemas.price_evaluation import CalculatePriceReq, EvaluateConfigUpdateReq
from dao.price_evaluation import FileDaoExtended, CostReportDao, CostPeopleDao, EvaluateConfigDao
import uuid

class PriceEvaluationService:
    @classmethod
    async def get_evaluate_config(cls):
        configs = await EvaluateConfigDao.get_all_config()
        return [{"key": config.key, "value": config.value, "annotation": config.annotation} for config in configs]

    @classmethod
    async def update_evaluate_config(cls, req: EvaluateConfigUpdateReq):
        update_data = {"value": req.value}
        if req.annotation is not None:
            update_data["annotation"] = req.annotation
        # 修改EvaluateConfigDao以支持字典，或者直接修改
        return await EvaluateConfigDao.update_config_dict(req.key, update_data)

    @classmethod
    async def calculate_price(cls, req: CalculatePriceReq):
        details = await CostDetailDao.get_by_file_id(req.file_id)
        if not details:
            raise Exception('No details found for the given file_id')
            
        file_info = await FileDaoExtended.get_file_by_id(req.file_id)
        if not file_info:
            raise Exception('File not found')
            
        cost_people = await CostPeopleDao.get_latest_cost_by_city(req.city)
        if not cost_people:
            raise Exception(f'Cost information not found for city: {req.city}')
            
        city_cost = cost_people.price
        
        # update ufp to us and calculate
        adjust_before_us_total = 0
        total_us = 0
        
        ei_total = 0
        eo_total = 0
        eq_total = 0
        ilf_total = 0
        eif_total = 0
        
        for item in details:
            ufp = item.ufp or 0
            
            # reuse_degree
            rd_val = 1
            if item.reuse_degree == '高':
                rd_val = 0.33
            elif item.reuse_degree == '中':
                rd_val = 0.66
                
            # repair_type
            rt_val = 1
            if item.repair_type == '新增':
                rt_val = 1
            elif item.repair_type == '修改':
                rt_val = 0.8
            elif item.repair_type == '删除':
                rt_val = 0.2
                
            us = ufp * rd_val * rt_val
            adjust_before_us_total += us
            
            # category count
            category = (item.function_category or '').upper()
            if category == 'EI':
                ei_total += 1
            elif category == 'EO':
                eo_total += 1
            elif category == 'EQ':
                eq_total += 1
            elif category == 'ILF':
                ilf_total += 1
            elif category == 'EIF':
                eif_total += 1
                
            await CostDetailDao.update_detail(item.id, {'us': us})
            
        adjust_before_us_total = round(adjust_before_us_total, 2)
        adjust_after_us_total = round(adjust_before_us_total * req.CF, 2)
        
        UE = req.PDR * adjust_after_us_total
        SWF = req.AT * req.QR
        AE = UE * SWF * req.XC
        F = city_cost / 1000
        
        total_price = (AE / req.HM) * F if req.HM else 0
        unit_price = total_price / adjust_before_us_total if adjust_before_us_total else 0
        
        existing_report = await CostReportDao.get_by_file_id(req.file_id)
        report_id = existing_report.report_id if existing_report else str(uuid.uuid4())
        
        report_data = {
            'report_id': report_id,
            'file_id': req.file_id,
            'file_name': file_info.file_name,
            'generator_user_id': file_info.uploader_user_id,
            'total_price': total_price,
            'unit_price': unit_price,
            'ei_total': ei_total,
            'eo_total': eo_total,
            'eq_total': eq_total,
            'ilf_total': ilf_total,
            'eif_total': eif_total,
            'adjust_before_us_total': adjust_before_us_total,
            'adjust_after_us_total': adjust_after_us_total,
            'cf': req.CF,
            'pdr': req.PDR,
            'at': req.AT,
            'qr': req.QR,
            'xc': req.XC,
            'hm': req.HM,
            'city_price': f"{req.city}(￥{int(city_cost) if city_cost == int(city_cost) else city_cost})"
        }
        
        if existing_report:
            saved_report = await CostReportDao.update_report(report_id, report_data)
        else:
            saved_report = await CostReportDao.create_report(report_data)
        
        return {
            'report_id': saved_report.report_id,
            'file_id': saved_report.file_id,
            'file_name': saved_report.file_name,
            'generator_user_id': saved_report.generator_user_id,
            'total_price': saved_report.total_price,
            'unit_price': saved_report.unit_price,
            'ei_total': saved_report.ei_total,
            'eo_total': saved_report.eo_total,
            'eq_total': saved_report.eq_total,
            'ilf_total': saved_report.ilf_total,
            'eif_total': saved_report.eif_total,
            'adjust_before_us_total': saved_report.adjust_before_us_total,
            'adjust_after_us_total': saved_report.adjust_after_us_total,
            'cf': saved_report.cf,
            'pdr': saved_report.pdr,
            'at': saved_report.at,
            'qr': saved_report.qr,
            'xc': saved_report.xc,
            'hm': saved_report.hm,
            'city_price': saved_report.city_price
        }


