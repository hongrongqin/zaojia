<template>
  <div class="evaluation-detail">
    <!-- 提示与操作区 -->
    <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
      <el-alert
        title="小提示：修改评估明细后请点击重新计算，计算造价报告"
        type="info"
        show-icon
        :closable="false"
        style="width: auto; padding: 5px 15px; margin-right: 15px;"
      />
    </div>

    <!-- 评估明细 -->
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
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDefaultEvalConfig, getCostDetailList, updateCostDetail } from '@/api/index'

const props = defineProps({
  fileId: {
    type: String,
    required: true
  }
})

const loading = ref(false)
const tableData = ref([])

const recalcLoading = ref(false)

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

const emit = defineEmits(['recalculate'])
const handleRecalculate = () => {
  // Trigger parent form calculation to ensure all parameters are included
  emit('recalculate')
}

const refreshData = () => {
  fetchList()
}

defineExpose({
  refreshData
})

// 监听 fileId 变化重新加载
watch(() => props.fileId, () => {
  fetchList()
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