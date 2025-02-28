<template>
	<el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @keyup.enter="onLogin">
		<div class="login-title">HxGPT</div>
		<el-form-item prop="username">
			<el-input v-model="loginForm.username" :prefix-icon="User" placeholder="用户名"></el-input>
		</el-form-item>
		<el-form-item prop="password">
			<el-input v-model="loginForm.password" :prefix-icon="Lock" show-password placeholder="密码"></el-input>
		</el-form-item>

		<el-form-item class="login-button">
			<el-button type="primary" @click="onLogin()">登录</el-button>
		</el-form-item>
	</el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import store from '@/store'
import { useRouter,useRoute } from 'vue-router'
import { isMobile } from '@/utils/tool'

const router = useRouter()
const loginFormRef = ref()

const route = useRoute()
const defaultUsername = route.query.username?.toString() || ''
const defaultPassword = route.query.password?.toString() || ''

const loginForm = reactive({
	username: defaultUsername,
	password: defaultPassword
})

const loginRules = ref({
	username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
	password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
})

onMounted(() => {
})

const onLogin = () => {
	loginFormRef.value.validate((valid: boolean) => {
		if (!valid) {
			return false
		}

		// 用户登录
		store.userStore
			.accountLoginAction(loginForm)
			.then(() => {
				if (!isMobile()) {
					router.push({ path: '/chat' })
				} else {
					// 手机端
					router.push({ path: '/chat_mobile' })
				}
			})
	})
}
</script>

<style lang="scss" scoped>
.login-title {
	display: flex;
	justify-content: center;
	margin-bottom: 35px;
	font-size: 24px;
	color: #444;
	letter-spacing: 4px;
}

.login-captcha {
	:deep(.el-input) {
		width: 200px;
	}
}

.login-captcha img {
	width: 150px;
	height: 40px;
	margin: 5px 0 0 10px;
	cursor: pointer;
}

.login-button {
	:deep(.el-button--primary) {
		margin-top: 10px;
		width: 100%;
		height: 45px;
		font-size: 18px;
		letter-spacing: 8px;
	}
}
</style>
