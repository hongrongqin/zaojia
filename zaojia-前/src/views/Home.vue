<template>
  <div class="home-container">
    <el-container class="layout-container">
      <el-header class="header">
        <div class="logo">
          <img src="/uploads/avatars/logo.jpg" alt="logo" class="sys-logo" />
          <span class="title">软件造价评估系统</span>
        </div>
        <el-menu
          :default-active="activeIndex"
          class="nav-menu"
          mode="horizontal"
          background-color="#409EFF"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
        >
          <el-menu-item index="/evaluation">项目评估</el-menu-item>
          <el-menu-item index="/standard">造价标准</el-menu-item>
          <el-menu-item index="/maintenance" v-if="roleType === '管理员'">数据维护</el-menu-item>
          <el-menu-item index="/center">个人中心</el-menu-item>
        </el-menu>
        <div class="user-info">
          <el-dropdown @command="handleCommand">
            <span class="el-dropdown-link">
              <el-avatar :size="32" icon="UserFilled" />
              <span class="username">{{ username }}</span>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Tools, UserFilled, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()

const roleType = ref(localStorage.getItem('role_type') || '')
const username = ref(localStorage.getItem('username') || '')

const activeIndex = computed(() => {
  return route.path
})

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('uid')
      localStorage.removeItem('username')
      localStorage.removeItem('role_type')
      router.push('/login')
      ElMessage.success('退出登录成功')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  width: 100vw;
}

.layout-container {
  height: 100%;
}

.header {
  background-color: #409EFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  width: 250px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 1px;
}

.sys-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.nav-menu {
  flex: 1;
  border-bottom: none !important;
  justify-content: center;
}

.nav-menu .el-menu-item {
  font-size: 16px;
  padding: 0 30px;
}

.user-info {
  width: 150px;
  display: flex;
  justify-content: flex-end;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  cursor: pointer;
  outline: none;
}

.username {
  font-size: 14px;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  box-sizing: border-box;
}

/* 过渡动画 */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>