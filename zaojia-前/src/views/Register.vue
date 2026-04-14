<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <div class="logo">
          <img src="/uploads/avatars/logo.jpg" alt="logo" />
        </div>
        <h2>注册新账号</h2>
        <p>加入软件造价自动评估系统</p>
      </div>
      
      <el-form 
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        label-position="top"
        size="large"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="registerForm.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="phone">
          <el-input 
            v-model="registerForm.phone" 
            placeholder="请输入手机号"
            prefix-icon="Phone"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="请确认密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-button type="success" class="register-btn" :loading="loading" @click="handleRegister">
          立即注册
        </el-button>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <el-link type="success" @click="$router.push('/login')">去登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, UserFilled, Phone } from '@element-plus/icons-vue'
import { register } from '@/api/login'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)

const registerForm = reactive({
  username: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      loading.value = true
      try {
        // 构造后端需要的参数（去除 confirmPassword）
        const data = {
          username: registerForm.username,
          password: registerForm.password,
          phone: registerForm.phone
        }
        
        // 调用后端注册接口
        const res = await register(data)
        
        // 此处的判断根据你后端的实际返回状态码为准，假设 code === 0 或 code === 200 为成功
        if (res.code === 0 || res.code === 200) {
          ElMessage.success('注册成功，请登录')
          router.push('/login')
        } else {
          ElMessage.error(res.msg || '注册失败')
        }
      } catch (error) {
        console.error('注册错误:', error)
        ElMessage.error('网络请求失败，请稍后重试')
      } finally {
        loading.value = false
      }
    } else {
      console.log('error submit!', fields)
    }
  })
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  /* background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); */
  /* 使用稍微不同的渐变色以此区分，或者保持一致 */
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  overflow: hidden;
  position: relative;
}

/* 保持一致的背景装饰 */
.register-container::before {
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

.register-container::after {
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

.register-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  z-index: 1;
  transition: transform 0.3s ease;
}

.register-box:hover {
  transform: translateY(-5px);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 60px;
  height: 60px;
  background: #f0f9eb;
  border-radius: 50%;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(103, 194, 58, 0.2);
  overflow: hidden;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.register-header h2 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 10px;
  font-weight: 600;
}

.register-header p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.register-form .el-input {
  --el-input-hover-border-color: #67C23A;
  --el-input-focus-border-color: #67C23A;
}

.register-btn {
  width: 100%;
  padding: 22px 0;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
  margin-top: 10px;
  background: linear-gradient(90deg, #67C23A, #529b2e);
  border: none;
  transition: all 0.3s;
}

.register-btn:hover {
  background: linear-gradient(90deg, #85ce61, #67C23A);
  box-shadow: 0 5px 15px rgba(103, 194, 58, 0.3);
  transform: translateY(-2px);
}

.register-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #606266;
}

.register-footer .el-link {
  font-size: 14px;
  vertical-align: baseline;
  margin-left: 5px;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .register-box {
    width: 90%;
    padding: 30px 20px;
  }
}
</style>
