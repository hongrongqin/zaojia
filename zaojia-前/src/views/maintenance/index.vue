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
          <el-table-column label="当前值" align="center">
            <template #default="scope">
              <el-input-number v-model="scope.row.value" :precision="2" :step="0.01" style="width: 150px" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" size="small" :loading="scope.row.loading" @click="updateConfig(scope.row)">
                更新
              </el-button>
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
            <el-select v-model="sortOrder" size="small" style="width: 120px; margin-right: 15px;" @change="sortData">
              <el-option label="价格降序" value="desc" />
              <el-option label="价格升序" value="asc" />
            </el-select>
            <el-button type="primary" size="small" @click="handleAdd" :icon="Plus">新增城市价格</el-button>
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
          <el-table-column label="操作" width="150" align="center">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)" :icon="Edit">
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      :title="dialogType === 'add' ? '新增城市价格' : '修改城市价格'"
      v-model="dialogVisible"
      width="400px"
      :close-on-click-modal="false"
      @close="closeDialog"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="城 市" prop="city">
          <el-input 
            v-model="form.city" 
            placeholder="请输入城市名称" 
            :disabled="dialogType === 'edit'"
          />
        </el-form-item>
        <el-form-item label="综合单价" prop="price">
          <el-input-number 
            v-model="form.price" 
            :min="0" 
            :precision="2" 
            :step="100" 
            placeholder="请输入价格"
            style="width: 100%;"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取 消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getDefaultEvalConfig, updateEvalConfig, getCostPeopleList, addCostPeople } from '@/api/index'

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

const dialogVisible = ref(false)
const dialogType = ref('add') // 'add' or 'edit'
const submitLoading = ref(false)
const formRef = ref(null)

const form = ref({
  city: '',
  price: undefined
})

const rules = {
  city: [{ required: true, message: '请输入城市名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入综合单价', trigger: 'blur' }]
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
        annotation: item.annotation,
        loading: false
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

// 更新单个配置项
const updateConfig = async (row) => {
  row.loading = true
  try {
    const payload = {
      key: row.key,
      value: Number(row.value),
      annotation: row.annotation
    }
    const res = await updateEvalConfig(payload)
    if (res && (res.code === 0 || res.code === 200)) {
      ElMessage.success(`${row.label} 更新成功`)
      await fetchConfig() // 刷新配置数据
    } else {
      ElMessage.error(res?.msg || '更新失败')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('网络异常，更新失败')
  } finally {
    row.loading = false
  }
}

// 获取列表数据
const fetchList = async () => {
  loading.value = true
  try {
    const res = await getCostPeopleList()
    // 由于后端有可能返回 code 等外层包裹，按照 request 拦截器如果只有 return res.data，那么 res 可能就是数据本身或者 res.data 是数据，取决于具体的拦截器。
    // 这里假设拦截器里没包 code 等，如果是按照 restful 直接返回数组:
    tableData.value = res.data || res || []
    sortData() // 拿到数据后立即排序
  } catch (error) {
    console.error(error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 新增
const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    city: '',
    price: undefined
  }
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = {
    city: row.city,
    price: row.price
  }
  dialogVisible.value = true
}

// 关闭弹窗
const closeDialog = () => {
  dialogVisible.value = false
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交
const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        await addCostPeople(form.value)
        ElMessage.success(dialogType.value === 'add' ? '新增成功' : '修改成功')
        closeDialog()
        fetchList()
      } catch (error) {
        console.error(error)
        ElMessage.error(dialogType.value === 'add' ? '新增失败' : '修改失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
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