<template>
  <div class="evaluation-container">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>个人中心 - 历史评估记录</span>
        </div>
      </template>
      <div class="content" v-loading="loading">
        <el-empty v-if="!historyList || historyList.length === 0" description="暂无历史对记录"></el-empty>
        <el-row :gutter="20" v-else>
          <el-col :span="8" v-for="item in historyList" :key="item.file_id" style="margin-bottom: 20px;">
            <el-card shadow="hover" class="history-card">
              <div class="card-content">
                <div class="file-icon">
                  <el-icon :size="40" color="#409eff"><Document /></el-icon>
                </div>
                <div class="file-info">
                  <h3 class="file-name" :title="item.file_name">{{ item.file_name }}</h3>
                  <p class="file-meta">
                    <el-tag size="small" type="info">{{ item.file_type }}</el-tag>
                  </p>
                  <p class="upload-time"><el-icon><Clock /></el-icon> {{ item.upload_time }}</p>
                </div>
              </div>
              <div class="card-actions">
                <el-button type="primary" plain size="small" @click="handleViewDetail(item)">查看详情</el-button>
                <el-popconfirm title="确定要删除这条记录吗？" @confirm="handleDelete(item)">
                  <template #reference>
                    <el-button type="danger" plain size="small">删除</el-button>
                  </template>
                </el-popconfirm>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="文件评估详情"
      width="70%"
      top="2vh"
      destroy-on-close
    >
      <report-detail v-if="currentFileId" :fileId="currentFileId" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Document, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useMainStore } from '@/store'
import ReportDetail from '@/views/center/report_detail.vue'
import { getHistoryList, deleteHistory } from '@/api/index'

const store = useMainStore()
const loading = ref(false)
const historyList = ref([])

// 弹窗与详情
const dialogVisible = ref(false)
const currentFileId = ref('')

// 获取用户ID，假设从pinia中获取
const userId = computed(() => store.userInfo?.userId || store.userInfo?.user_id || '')

const fetchHistory = async () => {
  // 实际应该传入真实用户ID
  const uid = userId.value || localStorage.getItem('uid') || ''
  loading.value = true
  try {
    const res = await getHistoryList(uid)
    if (res && (res.code === 0 || res.code === 200)) {
      historyList.value = res.data || []
    } else {
      ElMessage.error(res?.msg || '获取历史记录失败')
    }
  } catch (error) {
    console.error('获取历史记录异常:', error)
    ElMessage.error('网络异常，获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleViewDetail = (item) => {
  currentFileId.value = item.file_id
  dialogVisible.value = true
}

const handleDelete = async (item) => {
  try {
    const res = await deleteHistory(item.file_id)
    if (res && (res.code === 0 || res.code === 200)) {
      ElMessage.success('删除成功')
      fetchHistory() // 删除成功后重新拉取列表
    } else {
      ElMessage.error(res?.msg || '删除失败')
    }
  } catch (error) {
    console.error('删除历史记录异常:', error)
    ElMessage.error('网络异常，删除失败')
  }
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.evaluation-container {
  height: 100%;
  margin: 0 100px;
}
.card-header {
  font-weight: bold;
}
.content {
  min-height: 400px;
  padding: 0 10px;
}
:deep(.el-card__body) {
  padding: 20px 10px;
}
.history-card {
  border-radius: 8px;
  transition: all 0.3s;
}
.history-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.card-content {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}
.file-icon {
  margin-right: 15px;
  padding: 10px;
  background: #ecf5ff;
  border-radius: 8px;
}
.file-info {
  flex: 1;
  overflow: hidden;
}
.file-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.file-meta {
  margin: 0 0 5px 0;
}
.upload-time {
  margin: 0;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}
.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}
</style>