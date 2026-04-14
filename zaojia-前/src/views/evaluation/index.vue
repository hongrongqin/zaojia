<template>
  <div class="evaluation-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>项目评估</span>
        </div>
      </template>
      <div class="content">
        <!-- 操作流程说明 -->
        <el-alert
          title="操作流程"
          description="先上传文件，点击进行评估按钮，等待评估完成后自动展示结果"
          type="info"
          show-icon
          :closable="false"
          style="margin-bottom: 20px;"
        />

        <!-- 文件上传区域 -->
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :limit="1"
          accept=".txt,.doc,.docx,.pdf"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :on-exceed="handleExceed"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip text-center">
              支持上传 txt, doc, docx, pdf 格式文件
            </div>
          </template>
        </el-upload>

        <div class="evaluate-btn-wrapper">
          <el-button 
            type="primary" 
            size="large" 
            :loading="isEvaluating"
            :disabled="!selectedFile"
            @click="submitEvaluation"
          >
            进行评估
          </el-button>
        </div>

        <!-- 评估明细组件 -->
        <evaluation-detail ref="evalDetailRef" v-if="currentFileId" :file-id="currentFileId" @recalculate="startCalculate" />

        <!-- 评估计算配置表单和结果展示 -->
        <div v-if="currentFileId" class="calculation-section">
          <el-card shadow="never" class="calc-card">
            <template #header>
              <div class="card-header">
                <span>造价参数配置</span>
              </div>
            </template>
            <el-form :model="calcForm" label-width="210px" v-loading="loadingConfig">
              <el-row :gutter="20">
                <el-col :span="12" v-for="item in dynamicConfigs" :key="item.key">
                  <el-form-item :label="item.annotation || item.key">
                    <el-input-number v-model="calcForm.dynamicParams[item.key]" :step="0.01" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="所在城市">
                    <el-select v-model="calcForm.city" placeholder="请选择所在城市" style="width: 100%" :loading="loadingCities">
                      <el-option
                        v-for="item in cityOptions"
                        :key="item.city"
                        :label="`${item.city} (￥${item.price})`"
                        :value="item.city"
                      >
                        <span style="float: left">{{ item.city }}</span>
                        <span style="float: right; color: var(--el-text-color-secondary); font-size: 13px;">
                          ￥{{ item.price }}
                        </span>
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <div style="text-align: center; margin-top: 20px;">
                <el-button type="primary" size="large" @click="startCalculate" :loading="isCalculating">
                  开始计算
                </el-button>
              </div>
            </el-form>
          </el-card>

          <!-- 报告结果展示 -->
          <el-card v-if="reportData" shadow="never" class="result-card">
            <template #header>
              <div class="card-header">
                <span>造价评估报告</span>
              </div>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="文件名">{{ reportData.file_name }}</el-descriptions-item>
              <el-descriptions-item label="生成人ID">{{ reportData.generator_user_id }}</el-descriptions-item>
              <el-descriptions-item label="总价格(万元)">
                <span class="price-text">￥{{ formatMoney(reportData.total_price) }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="功能点单价(万元)">
                <span class="price-text">￥{{ formatMoney(reportData.unit_price) }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="总EI数量">{{ reportData.ei_total }}</el-descriptions-item>
              <el-descriptions-item label="总EO数量">{{ reportData.eo_total }}</el-descriptions-item>
              <el-descriptions-item label="总EQ数量">{{ reportData.eq_total }}</el-descriptions-item>
              <el-descriptions-item label="总ILF数量">{{ reportData.ilf_total }}</el-descriptions-item>
              <el-descriptions-item label="总EIF数量">{{ reportData.eif_total }}</el-descriptions-item>
              <el-descriptions-item label="调整前总功能点">{{ reportData.adjust_before_us_total }}</el-descriptions-item>
              <el-descriptions-item label="调整后总功能点">{{ reportData.adjust_after_us_total }}</el-descriptions-item>
              <el-descriptions-item label="所在城市及单价(元)">{{ reportData.city_price }}</el-descriptions-item>
              <el-descriptions-item v-for="item in dynamicConfigs" :key="item.key" :label="item.annotation || item.key">
                {{ reportData[item.key.toLowerCase()] ?? reportData[item.key] }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import EvaluationDetail from './evaluation_detail.vue'
import { getDefaultEvalConfig, getCostPeopleList, calculateEvaluation, uploadFile } from '@/api/index'

const selectedFile = ref(null)
const isEvaluating = ref(false)
const currentFileId = ref('')
const evalDetailRef = ref(null)

// 新增相关状态变量
const loadingConfig = ref(false)
const loadingCities = ref(false)
const isCalculating = ref(false)
const reportData = ref(null)

const cityOptions = ref([])

const calcForm = reactive({
  file_id: '',
  city: '',
  dynamicParams: {}
})

const dynamicConfigs = ref([])

// 格式化金额
const formatMoney = (val) => {
  if (val === null || val === undefined) return '0.00'
  return Number(val).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// 获取配置默认值
const fetchDefaultConfig = async () => {
  loadingConfig.value = true
  try {
    const res = await getDefaultEvalConfig()
    if (res && (res.code === 0 || res.code === 200)) {
      const data = res.data || []
      dynamicConfigs.value = data
      data.forEach(item => {
        calcForm.dynamicParams[item.key] = Number(item.value)
      })
    } else {
      ElMessage.warning(res?.msg || '获取默认配置失败')
    }
  } catch (error) {
    ElMessage.error('网络异常，获取默认配置失败')
  } finally {
    loadingConfig.value = false
  }
}

// 获取城市列表
const fetchCities = async () => {
  loadingCities.value = true
  try {
    const res = await getCostPeopleList()
    if (Array.isArray(res)) {
      cityOptions.value = res
    } else if (res && (res.code === 0 || res.code === 200)) {
      cityOptions.value = Array.isArray(res.data) ? res.data : (res.data?.list || res.data?.records || [])
    } else {
      ElMessage.warning(res?.msg || '获取城市列表失败')
    }
  } catch (error) {
    console.error('获取城市列表异常:', error)
    ElMessage.error('网络异常，获取城市列表失败')
  } finally {
    loadingCities.value = false
  }
}

// 监听文件ID变化，重置表单并拉取配置
watch(currentFileId, (newId) => {
  if (newId) {
    calcForm.file_id = newId
    reportData.value = null // 清空旧数据
    fetchDefaultConfig()
    fetchCities()
  }
})

// 开始计算
const startCalculate = async () => {
  if (!calcForm.file_id) {
    ElMessage.warning('文件ID丢失，请重新上传文件！')
    return
  }
  if (!calcForm.city) {
    ElMessage.warning('请选择所在城市！')
    return
  }

  isCalculating.value = true
  try {
    const payload = {
      file_id: calcForm.file_id,
      city: calcForm.city,
      ...calcForm.dynamicParams
    }
    const res = await calculateEvaluation(payload)
    
    if (res && (res.code === 0 || res.code === 200)) {
      ElMessage.success('计算成功！')
      reportData.value = res.data?.cost_report || res.data // 根据实际返回结构调整
      
      if (evalDetailRef.value) {
        evalDetailRef.value.refreshData()
      }
    } else {
      ElMessage.error(res?.msg || '计算失败')
    }
  } catch (error) {
    ElMessage.error('网络异常，估算计算失败')
  } finally {
    isCalculating.value = false
  }
}

const handleFileChange = (uploadFile) => {
  selectedFile.value = uploadFile.raw
  currentFileId.value = '' // 切换文件时清空明细
}

const handleFileRemove = () => {
  currentFileId.value = '' // 移除文件时清空明细
  selectedFile.value = null
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件，请先移除已选择的文件')
}

// 提交评估
const submitEvaluation = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择要上传的文件')
    return
  }

  const uid = localStorage.getItem('uid')
  if (!uid) {
    ElMessage.error('获取用户信息失败，请重新登录')
    return
  }

  isEvaluating.value = true

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('uploader_user_id', uid)

  try {
    const res = await uploadFile(formData)

    if (res && (res.code === 0 || res.code === 200)) {
      ElMessage.success('评估完成')
      // 评估完成后展示结果
      currentFileId.value = res.data?.file_id || res.data // 假设评估成功后返回file_id

    } else {
      ElMessage.error(res?.msg || '评估失败')
    }
  } catch (error) {
    console.error('评估请求异常:', error)
    ElMessage.error('网络异常，评估失败')
  } finally {
    isEvaluating.value = false
  }
}
</script>

<style scoped>
.evaluation-container {
  height: 100%;
  /* 控制整个容器的左右外边距，值越小边距越窄 */
  margin: 0 100px; /* 上下0，左右10px，可根据需要调整 */
}
.card-header {
  font-weight: bold;
}
.content {
  min-height: 400px;
  /* 控制内容区域的左右内边距，避免内容贴边 */
  padding: 0 10px; /* 上下0，左右10px，可根据需要调整 */
  display: flex;
  flex-direction: column;
}
.upload-demo {
  margin: 0 auto;
  width: 100%;
  max-width: 600px;
}
.text-center {
  text-align: center;
  margin-top: 10px;
  font-size: 13px;
  color: #909399;
}
.evaluate-btn-wrapper {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
.calculation-section {
  margin-top: 30px;
}
.calc-card {
  margin-bottom: 20px;
}
.result-card {
  margin-top: 20px;
}
.price-text {
  color: #f56c6c;
  font-weight: bold;
}
/* 可选：调整el-card本身的内边距 */
:deep(.el-card__body) {
  padding: 20px 10px; /* 上下20px，左右10px，默认是20px，缩小左右值 */
}
</style>