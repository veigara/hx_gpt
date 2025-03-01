import axios from 'axios'
import qs from 'qs'
import store from '@/store'
import { ElNotification } from 'element-plus'

// axios实例
const service = axios.create({
	baseURL: import.meta.env.VITE_API_URL as any,
	timeout: 60000,
	headers: { 'Content-Type': 'application/json;charset=UTF-8' }
})

// 请求拦截器
service.interceptors.request.use(
	(config: any) => {
		// 追加时间戳，防止GET请求缓存
		const userStore = store.userStore
		if (userStore?.token) {
			config.headers.Authorization = "Bearer "+userStore.token
		}
		if (config.method?.toUpperCase() === 'GET') {
			config.params = { ...config.params, t: new Date().getTime() }
		}
		if (Object.values(config.headers).includes('application/x-www-form-urlencoded')) {
			config.data = qs.stringify(config.data)
		}

		return config
	},
	error => {
		return Promise.reject(error)
	}
)

// 响应拦截器
service.interceptors.response.use(
	response => {
		if (response.status !== 200) {
			if(response.status === 401){
				// 没有权限，如：未登录、登录过期等，需要跳转到登录页
				store.userStore?.setToken('')
				location.reload()
				return
			}
			ElNotification({
				title: '错误',
				message: response.statusText,
				type: 'error',
				duration: 9500
			})
			return Promise.reject(new Error(response.statusText || 'Error'))
		}
		
		const res = response.data
		
		if(res.code &&  res.code !== 200){
			ElNotification({
				title: '错误',
				message: res.msg,
				type: 'error',
				duration: 9500
			})
			return Promise.reject(new Error(JSON.stringify(res.msg) || 'Error'))
		}

		// 响应成功
		return res;
	},
	error => {
		console.log(error)
		const status = error?.response.status
		if(status && status === 401){
			ElNotification({
				title: '错误',
				message: '登录过期，请重新登录',
				type: 'error',
				duration: 1000
			})
			store.userStore?.setToken('')
			location.reload()
			return	
		}
		const code= error?.code
		if(code && code === 'ERR_NETWORK'){
			ElNotification({
				title: '错误',
				message: '连接服务器失败',
				type: 'error',
				duration: 1000
			})
		}else{
			const msg = error.response.data?error.response.data:error.message
			ElNotification({
				title: '错误',
				message: msg,
				type: 'error',
				duration: 1000
			})
		}
		
		return Promise.reject(error)
	}
)

// 导出 axios 实例
export default service
