import request from '@/utils/request'

// ---- 默认配置与基础数据 ----
export const getDefaultEvalConfig = () => {
  return request.get('/price_evaluation/evaluate_config/default')
}

export const updateEvalConfig = (data) => {
  return request.put('/price_evaluation/evaluate_config/update', data)
}

export const getCostPeopleList = () => {
  return request.get('/management_maintenance/cost-people')
}

export const addCostPeople = (data) => {
  return request.post('/management_maintenance/cost-people', data)
}

// ---- 项目评估 ----
export const uploadFile = (data) => {
  return request.post('/price_evaluation/upload', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const calculateEvaluation = (data) => {
  return request.post('/price_evaluation/calculate', data)
}

export const getCostDetailList = (file_id) => {
  return request.get('/price_evaluation/cost_detail/list', { params: { file_id } })
}

export const updateCostDetail = (data) => {
  return request.put('/price_evaluation/cost_detail/update', data)
}

// ---- 个人中心 ----
export const getHistoryList = (user_id) => {
  return request.get('/person_center/history', { params: { user_id } })
}

export const deleteHistory = (file_id) => {
  return request.delete('/person_center/history', { params: { file_id } })
}

export const getReportData = (file_id) => {
  return request.get('/person_center/report', { params: { file_id } })
}

export const getFileInfo = (file_id) => {
  return request.get('/person_center/file_info', { params: { file_id } })
}
