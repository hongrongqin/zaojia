<template>
  <div class="evaluation-container">
    <!-- 系统默认评估配置 -->
    <el-card shadow="never" class="config-card">
      <template #header>
        <div class="card-header">
          <span>系统默认评估配置</span>
        </div>
      </template>
      <div class="content">
        <el-table :data="configList" border stripe style="width: 100%" v-loading="configLoading">
          <el-table-column type="index" label="序号" width="80" align="center" />
          <el-table-column prop="label" label="配置项" align="center" />
          <el-table-column prop="key" label="参数名" align="center" />
          <el-table-column prop="value" label="当前值" align="center">
            <template #default="scope">
              {{ scope.row.value }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-card shadow="never" class="rate-card">
      <template #header>
        <div class="card-header">
          <span>软件开发基准人月费率</span>
          <div class="header-actions">
            <el-select v-model="sortOrder" size="small" style="width: 120px;" @change="sortData">
              <el-option label="价格降序" value="desc" />
              <el-option label="价格升序" value="asc" />
            </el-select>
          </div>
        </div>
      </template>
      <div class="content">
        <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
          <el-table-column type="index" label="序号" width="80" align="center" />
          <el-table-column prop="city" label="城市" align="center" />
          <el-table-column prop="price" label="综合单价 (元)" align="center">
            <template #default="scope">
              <span style="color: #f56c6c; font-weight: bold;">￥{{ scope.row.price }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDefaultEvalConfig, getCostPeopleList } from '@/api/index'

const loading = ref(false)
const tableData = ref([])
const sortOrder = ref('desc')

// 默认配置相关状态
const configLoading = ref(false)
const configList = ref([])
const configLabels = {
  scale_change_factor: '规模变更因子',
  productivity: '软件开发生产率',
  tcf: '技术复杂度(TCF)',
  average_monthly_working_days: '月均工作天数',
  average_daily_working_hours: '日均工作时长',
  high_degree: '高重用程度'
}

// 排序功能
const sortData = () => {
  if (!tableData.value || tableData.value.length === 0) return
  tableData.value.sort((a, b) => {
    return sortOrder.value === 'desc' ? b.price - a.price : a.price - b.price
  })
}

// 获取系统默认评估配置
const fetchConfig = async () => {
  configLoading.value = true
  try {
    const res = await getDefaultEvalConfig()
    if (res && (res.code === 0 || res.code === 200)) {
      const data = res.data || []
      configList.value = data.map(item => ({
        key: item.key,
        label: item.annotation || item.key,
        value: Number(item.value),
        annotation: item.annotation
      }))
    } else {
      ElMessage.warning(res?.msg || '获取默认配置失败')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('获取默认配置异常')
  } finally {
    configLoading.value = false
  }
}

// 获取列表数据
const fetchList = async () => {
  loading.value = true
  try {
    const res = await getCostPeopleList()
    tableData.value = res.data || res || []
    sortData() // 拿到数据后立即排序
  } catch (error) {
    console.error(error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchList()
  fetchConfig()
})
</script>

<style scoped>
.evaluation-container {
  height: 100%;
  margin: 0 100px;
}
.config-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}
.header-actions {
  display: flex;
  align-items: center;
}
.content {
  min-height: 400px;
  padding: 0 10px;
}
:deep(.el-card__body) {
  padding: 20px 10px;
}
</style>