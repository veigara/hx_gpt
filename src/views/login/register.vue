<template>
	<el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" @keyup.enter="onRegister">
		<div class="register-title">HxGPT</div>
		<el-form-item prop="username">
			<el-input v-model="registerForm.username" :prefix-icon="User" placeholder="用户名"></el-input>
		</el-form-item>
		<el-form-item prop="password">
			<el-input v-model="registerForm.password" :prefix-icon="Lock" show-password placeholder="密码"></el-input>
		</el-form-item>
		<el-form-item prop="password1">
			<el-input v-model="registerForm.password1" :prefix-icon="Lock" show-password placeholder="密码确认"></el-input>
		</el-form-item>
		<el-form-item class="register-button">
			<el-button type="primary" @click="onRegister()">注册</el-button>
		</el-form-item>
	</el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
import { useUserRegisterApi } from '@/api/login'


const router = useRouter()
const registerFormRef = ref()

const registerForm = reactive({
	username: '',
	password: '',
	password1: ''
})

const registerRules = ref({
	username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
	password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
	password1: [{ required: true, message: '密码确认不能为空', trigger: 'blur' }],
})

onMounted(() => {
})

const onRegister = () => {
	registerFormRef.value.validate((valid: boolean) => {
		if (!valid) {
			return false
		}
		if (registerForm.password !== registerForm.password1) {
			ElNotification({
				title: '密码',
				message: '两次密码输入不一致,请重新输入',
				type: 'error'
			})
			return false
		}
		useUserRegisterApi(registerForm).then((res: any) => {
			if (res.code === 200) {
				ElNotification({
					title: '注册成功',
					message: '请登录',
					type: 'success'
				})
				router.push({ path: '/login', query: { loginType: 'account', username: registerForm.username, password: registerForm.password } })
				// 刷新
				location.reload()
			} else {
				ElNotification({
					title: '注册失败',
					message: res.msg,
					type: 'error'
				})
			}
		})
	})
}
</script>

<style lang="scss" scoped>
.register-title {
	display: flex;
	justify-content: center;
	margin-bottom: 35px;
	font-size: 24px;
	color: #fff;
	letter-spacing: 4px;
}

.register-captcha {
	:deep(.el-input) {
		width: 200px;
	}
}

.register-captcha img {
	width: 150px;
	height: 40px;
	margin: 5px 0 0 10px;
	cursor: pointer;
}

.register-button {
	:deep(.el-button--primary) {
		margin-top: 10px;
		width: 100%;
		height: 45px;
		font-size: 18px;
		letter-spacing: 8px;
	}
}
</style>
