from dao.person_centor import PersonCentorDao

class PersonCentorService:
    @classmethod
    async def get_user_history(cls, user_id: str):
        records = await PersonCentorDao.get_history_by_user_id(user_id)
        # 根据请求返回对应字段信息
        return [
            {
                "file_id": r.file_id,
                "file_name": r.file_name,
                "file_content": r.file_content,
                "file_type": r.file_type,
                "file_storage_path": r.file_storage_path,
                "uploader_user_id": r.uploader_user_id,
                "upload_time": r.upload_time.strftime("%Y-%m-%d %H:%M:%S") if r.upload_time else None
            }
            for r in records
        ]

    @classmethod
    async def delete_history_by_file_id(cls, file_id: str):
        return await PersonCentorDao.delete_history_by_file_id(file_id)

    @classmethod
    async def get_report_by_file_id(cls, file_id: str):
        report = await PersonCentorDao.get_report_by_file_id(file_id)
        if not report:
            return None
        return {
            "report_id": report.report_id,
            "file_id": report.file_id,
            "file_name": report.file_name,
            "generator_user_id": report.generator_user_id,
            "total_price": report.total_price,
            "unit_price": report.unit_price,
            "ei_total": report.ei_total,
            "eo_total": report.eo_total,
            "eq_total": report.eq_total,
            "ilf_total": report.ilf_total,
            "eif_total": report.eif_total,
            "adjust_before_us_total": report.adjust_before_us_total,
            "adjust_after_us_total": report.adjust_after_us_total,
            "cf": report.cf,
            "pdr": report.pdr,
            "at": report.at,
            "qr": report.qr,
            "xc": report.xc,
            "hm": report.hm,
            "city_price": report.city_price,
            "generate_time": report.generate_time.strftime("%Y-%m-%d %H:%M:%S") if report.generate_time else None,
            "update_time": report.update_time.strftime("%Y-%m-%d %H:%M:%S") if report.update_time else None
        }

    @classmethod
    async def get_file_info_by_id(cls, file_id: str):
        file_info = await PersonCentorDao.get_file_info_by_id(file_id)
        if not file_info:
            return None
        return {
            "file_name": file_info.file_name,
            "file_content": file_info.file_content,
            "file_type": file_info.file_type
        }
