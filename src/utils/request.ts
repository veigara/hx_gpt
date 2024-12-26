import axios from 'axios'
import qs from 'qs'
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
		if (config.method?.toUpperCase() === 'GET') {
			config.params = { ...config.params, t: new Date().getTime() }
		}
		// 添加请求参数
		config.headers["authorization"]= "zhouhx"
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
			return Promise.reject(new Error(response.statusText || 'Error'))
		}

		// 响应成功
		return res;
	},
	error => {
		console.log(error)
		const msg = error.response.data?error.response.data:error.message
		ElNotification({
			title: '错误',
			message: msg,
			type: 'error',
			duration: 9500
		})
		return Promise.reject(error)
	}
)

// 导出 axios 实例
export default service
