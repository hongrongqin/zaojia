<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo">
          <img src="/uploads/avatars/logo.jpg" alt="logo" />
        </div>
        <h2>软件造价自动评估系统</h2>
        <p>欢迎回到系统</p>
      </div>
      
      <el-form 
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        label-position="top"
        size="large"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="captcha">
          <div class="captcha-box">
            <el-input 
              v-model="loginForm.captcha" 
              placeholder="请输入验证码"
              prefix-icon="Key"
            />
            <div class="captcha-img" @click="refreshCaptcha" title="点击刷新验证码">
              <img :src="captchaUrl" alt="验证码" v-if="captchaUrl"/>
              <span v-else>Loading...</span>
            </div>
          </div>
        </el-form-item>
        
        <el-button type="primary" class="login-btn" :loading="loading" @click="handleLogin">
          立即登录
        </el-button>
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Key, Tools } from '@element-plus/icons-vue'
import { getCodeImg, login } from '@/api/login'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const captchaUrl = ref('')

const loginForm = reactive({
  username: '',
  password: '',
  captcha: '',
  uuid: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 4, message: '验证码长度为4位', trigger: 'blur' }
  ]
}

// 获取验证码
const refreshCaptcha = async () => {
  try {
    const res = await getCodeImg()
    if (res.code === 0) {
      captchaUrl.value = res.data.img
      loginForm.uuid = res.data.uuid
    } else {
      ElMessage.error(res.msg || '获取验证码失败')
    }
  } catch (error) {
    console.error('获取验证码失败:', error)
  }
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid, fields) => {
    if (!valid) {
      console.log('error submit!', fields)
      return
    }

    loading.value = true
    try {
      const res = await login(loginForm.username, loginForm.password, loginForm.captcha, loginForm.uuid)

      if (res && (res.code === 0 || res.code === 200)) {
        const data = res.data || res
        const token = data.access_token || data.token
        if (token) {
          localStorage.setItem('token', token)
          if (data.uid) localStorage.setItem('uid', data.uid)
          if (data.username) localStorage.setItem('username', data.username)
          if (data.role_type) localStorage.setItem('role_type', data.role_type)
        }
        ElMessage.success('登录成功')
        router.push('/')
      } else {
        ElMessage.error(res?.msg || '登录失败')
        refreshCaptcha()
      }
    } catch (err) {
      console.error('登录请求失败:', err)
      ElMessage.error('网络异常，登录失败')
      refreshCaptcha()
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  refreshCaptcha()
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  overflow: hidden;
  position: relative;
}

/* 添加一些背景装饰 */
.login-container::before {
  content: '';
  position: absolute;
  width: 2000px;
  height: 2000px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  top: -10%;
  right: 48%;
  transform: translateY(-50%);
  z-index: 0;
}

.login-container::after {
  content: '';
  position: absolute;
  width: 1500px;
  height: 1500px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  bottom: -10%;
  left: 30%;
  transform: translateY(50%);
  z-index: 0;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  z-index: 1;
  transition: transform 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  background: #ecf5ff;
  border-radius: 50%;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(64, 158, 255, 0.2);
  overflow: hidden;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.login-header h2 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 10px;
  font-weight: 600;
}

.login-header p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.login-form .el-input {
  --el-input-hover-border-color: #409EFF;
  --el-input-focus-border-color: #409EFF;
}

.captcha-box {
  display: flex;
  gap: 12px;
}

.captcha-img {
  width: 170px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.captcha-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.login-btn {
  width: 100%;
  padding: 22px 0;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
  margin-top: 10px;
  background: linear-gradient(90deg, #409EFF, #3a8ee6);
  border: none;
  transition: all 0.3s;
}

.login-btn:hover {
  background: linear-gradient(90deg, #66b1ff, #409EFF);
  box-shadow: 0 5px 15px rgba(64, 158, 255, 0.3);
  transform: translateY(-2px);
}

.login-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

.login-footer .el-link {
  font-size: 14px;
  vertical-align: baseline;
  margin-left: 5px;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .login-box {
    width: 90%;
    padding: 30px 20px;
  }
}
</style>
