import { defineStore } from 'pinia'
import { useUserLoginApi} from '@/api/login'
import cache from '@/utils/cache'

export const userStore = defineStore('userStore', {
	state: () => ({
		// 用户信息
		user: {
			id: '',
			username: ''
		},
		// 登录token
		token: cache.getToken()
	}),
	actions: {
		setUser(val: any) {
			this.user = val
		},
		setToken(val: any) {
			this.token = val
			cache.setToken(val)
		},
		// 账号登录
		async accountLoginAction(loginForm: any) {
			const { data } = await useUserLoginApi(loginForm)
			this.setToken(data.access)
		}
	}
})
