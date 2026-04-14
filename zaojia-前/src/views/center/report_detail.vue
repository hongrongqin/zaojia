<template>
  <div class="evaluation-detail">
    <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
      <el-alert
        title="小提示：修改评估明细后请点击重新计算，计算造价报告"
        type="info"
        show-icon
        :closable="false"
        style="width: auto; padding: 5px 15px; margin-right: 15px;"
      />
      <div style="white-space: nowrap;">
        <el-button type="primary" @click="handleDownloadReport">下载造价报告</el-button>
        <el-button type="success" @click="handleDownloadDetail">下载评估明细</el-button>
        <el-button type="warning" @click="handleRecalculateDialog">重新计算</el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" type="border-card">
      <!-- 造价报告 Tab -->
      <el-tab-pane label="造价报告" name="report">
        <div v-loading="reportLoading" class="report-content">
          <el-empty v-if="!reportData || !reportData.report_id" description="暂无造价报告数据"></el-empty>
          <el-descriptions v-else title="造价报告信息" :column="2" border>
            <el-descriptions-item label="文档名称">{{ reportData.file_name }}</el-descriptions-item>
            <el-descriptions-item label="生成时间">{{ reportData.generate_time }}</el-descriptions-item>
            
            <el-descriptions-item label="总造价(万元)">
              <span style="color: #f56c6c; font-weight: bold; font-size: 16px;">￥{{ reportData.total_price }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="功能点单价(万元)">￥{{ reportData.unit_price }}</el-descriptions-item>
            <el-descriptions-item label="内部逻辑文件(ILF)总计">{{ reportData.ilf_total }}</el-descriptions-item>
            <el-descriptions-item label="外部接口文件(EIF)总计">{{ reportData.eif_total }}</el-descriptions-item>
            <el-descriptions-item label="外部输入(EI)总计">{{ reportData.ei_total }}</el-descriptions-item>
            <el-descriptions-item label="外部输出(EO)总计">{{ reportData.eo_total }}</el-descriptions-item>
            <el-descriptions-item label="外部查询(EQ)总计">{{ reportData.eq_total }}</el-descriptions-item>
            <el-descriptions-item label="调整前功能点总计">{{ reportData.adjust_before_us_total }}</el-descriptions-item>
            <el-descriptions-item label="调整后功能点总计">{{ reportData.adjust_after_us_total }}</el-descriptions-item>
            <el-descriptions-item label="所在城市及单价(元)" v-if="reportData.city_price">{{ reportData.city_price }}</el-descriptions-item>

            <el-descriptions-item v-for="item in dynamicConfigs" :key="item.key" :label="item.annotation || item.key">
              {{ reportData[item.key.toLowerCase()] ?? reportData[item.key] }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-tab-pane>

      <!-- 评估明细 Tab -->
      <el-tab-pane label="评估明细" name="detail">
        <el-table
          v-loading="loading"
          :data="tableData"
          style="width: 100%"
          height="500"
          border
          stripe
        >
          <el-table-column prop="item_name" label="功能点计数项名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="function_category" label="功能点类别" width="120" />
          <el-table-column prop="ufp" label="UFP" width="80" />
          <el-table-column prop="reuse_degree" label="复用程度" width="100" />
          <el-table-column prop="us" label="调整系数(US)" width="120" />
          <el-table-column prop="repair_type" label="修改类型" width="120" align="center" />
          <el-table-column prop="comment" label="备注" min-width="150" show-overflow-tooltip />
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <!-- 评估文件 Tab -->
      <el-tab-pane label="评估文件" name="file">
        <div v-loading="fileLoading" class="file-content" style="padding: 20px;">
          <el-empty v-if="!fileData || !fileData.file_name" description="暂无评估文件数据"></el-empty>
          <div v-else>
            <h3 style="margin-top: 0;">{{ fileData.file_name }}</h3>
            <p style="color: #666; margin-bottom: 20px;"><strong>文件类型：</strong>{{ fileData.file_type }}</p>
            <el-card shadow="never" style="background-color: #f8f9fa;">
              <pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0; font-family: inherit;">{{ fileData.file_content }}</pre>
            </el-card>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑明细"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="editForm"
        :rules="rules"
        label-width="140px"
      >
        <el-form-item label="功能点计数项名称" prop="item_name">
          <el-input v-model="editForm.item_name" placeholder="请输入功能点名称" />
        </el-form-item>
        <el-form-item label="功能点类别" prop="function_category">
          <el-select v-model="editForm.function_category" placeholder="请选择类别" style="width: 100%">
            <el-option label="内部逻辑文件(ILF)" value="ILF" />
            <el-option label="外部接口文件(EIF)" value="EIF" />
            <el-option label="外部输入(EI)" value="EI" />
            <el-option label="外部输出(EO)" value="EO" />
            <el-option label="外部查询(EQ)" value="EQ" />
          </el-select>
        </el-form-item>
        <el-form-item label="调整系数(US)" prop="us">
          <el-input-number v-model="editForm.us" :precision="2" :step="0.1" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="修改类型" prop="repair_type">
          <el-select v-model="editForm.repair_type" placeholder="请选择修改类型" style="width: 100%">
            <el-option label="新增" value="新增" />
            <el-option label="修改" value="修改" />
            <el-option label="删除" value="删除" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="comment">
          <el-input v-model="editForm.comment" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitLoading" @click="submitEdit">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 重新计算弹窗 -->
    <el-dialog
      v-model="recalcDialogVisible"
      title="确认计算参数"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-form :model="recalcForm" label-width="150px" v-loading="recalcFormLoading">
        <el-form-item label="规模变更因子(CF)">
          <el-input-number v-model="recalcForm.cf" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="生产率(PDR)">
          <el-input-number v-model="recalcForm.pdr" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="应用类型因子(AT)">
          <el-input-number v-model="recalcForm.at" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="质量特性因子(QR)">
          <el-input-number v-model="recalcForm.qr" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="信创调整系数(XC)">
          <el-input-number v-model="recalcForm.xc" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="人月折算系数(HM)">
          <el-input-number v-model="recalcForm.hm" :step="0.1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="所在城市及单价">
          <el-select v-model="recalcForm.city" placeholder="请选择城市" style="width: 100%">
            <el-option
              v-for="item in cityOptions"
              :key="item.city"
              :label="`${item.city}(￥${item.price})`"
              :value="item.city"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="recalcDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="recalcSubmitLoading" @click="submitRecalculate">确认计算</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'
import {
  getDefaultEvalConfig,
  getCostDetailList,
  getReportData,
  getFileInfo,
  updateCostDetail,
  getCostPeopleList,
  calculateEvaluation
} from '@/api/index'

const props = defineProps({
  fileId: {
    type: String,
    required: true
  }
})

const activeTab = ref('report')
const loading = ref(false)
const tableData = ref([])

const reportLoading = ref(false)
const reportData = ref({})
const recalcLoading = ref(false)

const fileLoading = ref(false)
const fileData = ref({})

const dynamicConfigs = ref([])

// 获取配置默认值以展示对应的名称
const fetchDefaultConfig = async () => {
  try {
    const res = await getDefaultEvalConfig()
    if (res && (res.code === 0 || res.code === 200)) {
      dynamicConfigs.value = res.data || []
    }
  } catch (error) {
    console.error('获取默认配置异常:', error)
  }
}

// 弹窗相关
const dialogVisible = ref(false)
const submitLoading = ref(false)
const formRef = ref(null)
const editForm = ref({
  id: '',
  item_name: '',
  function_category: '',
  repair_type: '修改',
  us: 1,
  comment: ''
})

const rules = {
  item_name: [{ required: true, message: '请输入功能点名称', trigger: 'blur' }],
  function_category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  repair_type: [{ required: true, message: '请选择修改类型', trigger: 'change' }]
}

// 获取明细列表数据
const fetchList = async () => {
  if (!props.fileId) return
  
  loading.value = true
  try {
    const res = await getCostDetailList(props.fileId)
    
    if (res && (res.code === 0 || res.code === 200)) {
      tableData.value = res.data || []
    } else {
      ElMessage.error(res?.msg || '获取明细列表失败')
    }
  } catch (error) {
    console.error('获取明细列表异常:', error)
    ElMessage.error('网络异常，获取数据失败')
  } finally {
    loading.value = false
  }
}

// 获取造价报告数据
const fetchReport = async () => {
  if (!props.fileId) return
  
  reportLoading.value = true
  try {
    const res = await getReportData(props.fileId)
    if (res && (res.code === 0 || res.code === 200)) {
      reportData.value = res.data || {}
    } else {
      ElMessage.error(res?.msg || '获取造价报告失败')
    }
  } catch (error) {
    console.error('获取造价报告异常:', error)
    ElMessage.error('网络异常，获取数据失败')
  } finally {
    reportLoading.value = false
  }
}

// 获取评估文件内容
const fetchFileInfo = async () => {
  if (!props.fileId) return
  
  fileLoading.value = true
  try {
    const res = await getFileInfo(props.fileId)
    if (res && (res.code === 0 || res.code === 200)) {
      fileData.value = res.data || {}
    } else {
      ElMessage.error(res?.msg || '获取评估文件失败')
    }
  } catch (error) {
    console.error('获取评估文件异常:', error)
    ElMessage.error('网络异常，获取评估文件数据失败')
  } finally {
    fileLoading.value = false
  }
}

// 重新评估的参数可以通过后端从数据库默认读取，如果不涉及特定表单传参。
// 为了和外部保持一致，这里可能需要传入配置或者我们自己发后端计算。
// 目前由于不知道是否需要强制带入所有参数，先移除原有只传file_id可能抛出错误的调用，改成触发父组件的计算事件
const emit = defineEmits(['recalculate'])

const recalcDialogVisible = ref(false)
const recalcFormLoading = ref(false)
const recalcSubmitLoading = ref(false)
const cityOptions = ref([])

const recalcForm = ref({
  cf: 1,
  pdr: 1,
  at: 1,
  qr: 1,
  xc: 1,
  hm: 1,
  city: ''
})

const handleRecalculateDialog = async () => {
  if (!props.fileId) return
  
  recalcDialogVisible.value = true
  recalcFormLoading.value = true
  
  try {
    // 获取城市列表
    const cityRes = await getCostPeopleList()
    if (cityRes) {
      cityOptions.value = Array.isArray(cityRes.data) ? cityRes.data : (Array.isArray(cityRes) ? cityRes : [])
    }

    // 获取当前报告已有数据填入参数
    const rdRes = await getReportData(props.fileId)
    if (rdRes && (rdRes.code === 0 || rdRes.code === 200)) {
      const rd = rdRes.data || {}
      
      // city_price: "太原(￥ 22920)"，需要提取出"太原"
      let currentCity = ''
      if (rd.city_price) {
        currentCity = rd.city_price.split('(')[0].trim() || rd.city_price.split('（')[0].trim()
      }
      
      recalcForm.value = {
        cf: Number(rd.cf) || Number(rd.scale_change_factor) || 1,
        pdr: Number(rd.pdr) || Number(rd.productivity) || 1,
        at: Number(rd.at) || 1,
        qr: Number(rd.qr) || Number(rd.quality_factor) || 1,
        xc: Number(rd.xc) || 1,
        hm: Number(rd.hm) || 1,
        city: currentCity
      }
    }
  } catch (error) {
    console.error('获取重算参数失败', error)
    ElMessage.error('获取重算参数失败')
  } finally {
    recalcFormLoading.value = false
  }
}

const submitRecalculate = async () => {
  if (!recalcForm.value.city) {
    ElMessage.warning('请选择城市')
    return
  }

  recalcSubmitLoading.value = true
  try {
    const payload = {
      file_id: props.fileId,
      CF: recalcForm.value.cf,
      PDR: recalcForm.value.pdr,
      AT: recalcForm.value.at,
      QR: recalcForm.value.qr,
      XC: recalcForm.value.xc,
      HM: recalcForm.value.hm,
      city: recalcForm.value.city
    }
    
    const res = await calculateEvaluation(payload)
    if (res && (res.code === 0 || res.code === 200)) {
      ElMessage.success('重新计算成功')
      recalcDialogVisible.value = false
      refreshData()
      emit('recalculate')
    } else {
      ElMessage.error(res?.msg || '重新计算失败')
    }
  } catch (error) {
    console.error('提交重算失败', error)
    ElMessage.error('网络异常，重新计算失败')
  } finally {
    recalcSubmitLoading.value = false
  }
}

const refreshData = () => {
  fetchList()
  fetchReport()
  fetchFileInfo()
}

defineExpose({
  refreshData
})

// 监听 fileId 变化重新加载
watch(() => props.fileId, () => {
  fetchList()
  fetchReport()
  fetchFileInfo()
}, { immediate: true })

onMounted(() => {
  fetchDefaultConfig()
})

// 点击编辑
const handleEdit = (row) => {
  editForm.value = {
    id: row.id,
    item_name: row.item_name,
    function_category: row.function_category,
    repair_type: row.repair_type || '修改',
    us: Number(row.us) || 1,
    comment: row.comment || ''
  }
  dialogVisible.value = true
}

// 下载评估明细
const handleDownloadDetail = async () => {
  if (!props.fileId) return
  ElMessage.info('正在下载评估明细...')
  try {
    const res = await getCostDetailList(props.fileId)
    
    if (res && (res.code === 0 || res.code === 200)) {
      const data = res.data || []
      const excelData = data.map(item => ({
        '功能点计数项名称': item.item_name,
        '类别': item.function_category,
        'UFP': item.ufp,
        '重用程度': item.reuse_degree,
        '修改类型': item.repair_type,
        'US': item.us,
        '备注': item.comment
      }))
      
      const ws = XLSX.utils.json_to_sheet(excelData)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, '评估明细')
      XLSX.writeFile(wb, `评估明细_${props.fileId}.xlsx`)
      ElMessage.success('下载成功')
    } else {
      ElMessage.error(res?.msg || '获取明细数据失败')
    }
  } catch (error) {
    console.error('下载明细异常:', error)
    ElMessage.error('网络异常，下载失败')
  }
}

// 下载造价报告
const handleDownloadReport = () => {
  if (!reportData.value || !reportData.value.report_id) {
    ElMessage.warning('暂无造价报告数据')
    return
  }
  
  const rd = reportData.value
  const rows = [
    ['文档名称', rd.file_name, '生成时间', rd.generate_time],
    ['总造价(万元)', `￥${rd.total_price || 0}`, '综合单价(万元)', `￥${rd.unit_price || 0}`],
    ['内部逻辑文件(ILF)总计', rd.ilf_total || 0, '外部接口文件(EIF)总计', rd.eif_total || 0],
    ['外部输入(EI)总计', rd.ei_total || 0, '外部输出(EO)总计', rd.eo_total || 0],
    ['外部查询(EQ)总计', rd.eq_total || 0, '调整前功能点总计', rd.adjust_before_us_total || 0],
    ['调整后功能点总计', rd.adjust_after_us_total || 0, '所在城市及单价(元)', rd.city_price || '']
  ]
  
  const dynamicRows = []
  if (dynamicConfigs.value && dynamicConfigs.value.length > 0) {
    for (let i = 0; i < dynamicConfigs.value.length; i += 2) {
      const item1 = dynamicConfigs.value[i]
      const item2 = dynamicConfigs.value[i + 1]
      
      const val1 = rd[item1.key.toLowerCase()] ?? rd[item1.key] ?? ''
      const l1 = item1.annotation || item1.key
      
      if (item2) {
        const val2 = rd[item2.key.toLowerCase()] ?? rd[item2.key] ?? ''
        const l2 = item2.annotation || item2.key
        dynamicRows.push([l1, val1, l2, val2])
      } else {
        dynamicRows.push([l1, val1, '', ''])
      }
    }
  }
  
  const allRows = [...rows, ...dynamicRows]
  
  const ws = XLSX.utils.aoa_to_sheet([
    ['造价报告信息', '', '', ''], // 表头
    ...allRows
  ])
  
  // 合并第一行标题
  ws['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 3 } }
  ]
  
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '造价报告')
  XLSX.writeFile(wb, `造价报告_${rd.file_name || props.fileId}.xlsx`)
}

// 提交编辑
const submitEdit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        const res = await updateCostDetail(editForm.value)
        
        if (res && (res.code === 0 || res.code === 200)) {
          ElMessage.success('更新成功')
          dialogVisible.value = false
          fetchList()
        } else {
          ElMessage.error(res?.msg || '更新失败')
        }
      } catch (error) {
        console.error('更新明细异常:', error)
        ElMessage.error('网络异常，更新失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}
</script>

<style scoped>
.evaluation-detail {
  margin-top: 20px;
}
.card-header {
  font-weight: bold;
}
</style>