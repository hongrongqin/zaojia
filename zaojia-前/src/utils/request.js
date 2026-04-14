import SystemConfig from '../config/SystemConfig'
import axios from 'axios'

axios.defaults.baseURL = SystemConfig.BASE_URL


axios.interceptors.request.use(config => {
    const token = localStorage.getItem("token")
    config.headers.Authorization = `Bearer ${token}`

    console.log("请求拦截：",config)
    return config
})

// 设置响应拦截器
axios.interceptors.response.use(res => {
    console.log("响应拦截器:", res)
    // 对应后端未授权错误码1002
    if (res.data.code === "1002") {
        window.localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(new Error('身份认证失败,请重新登录'))
    }
    return res.data
    // return res
}, err => {
    return Promise.reject(new Error(err))
})

export default axios