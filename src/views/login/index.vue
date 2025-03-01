<template>
	<div class="login-container">
		<div class="login-intro">
		</div>
		<div class="login-form">
			<Register v-if="loginType == 'register'"></Register>
			<account v-else></account>			
			<div class="login-more">
				<el-button text v-if="loginType == 'register'" type="success" link @click="loginSwitch('account')">登录</el-button>
				<el-button  text v-else type="success" link @click="loginSwitch('register')">注册</el-button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Account from './account.vue'
import Register from './register.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const reLoginType = route.query.loginType?.toString() || 'account'

// 登录类型
const loginType = ref(reLoginType)
const loginSwitch = (type: string) => {
	loginType.value = type
}
</script>

<style lang="scss" scoped>
.login-container {
	display: flex;
	justify-content: space-evenly;
	align-items: center;
	height: 100vh;
	background-image: url('@/assets/login.jpg'); /* 添加背景图片 */
	background-size: cover; /* 确保图片覆盖整个背景 */
	background-position: center; /* 图片居中 */
}
.login-intro {
	display: flex;
	flex-direction: column;
	width: 520px;
	flex: 0 1 auto;
}
.login-intro h1 {
	color: var(--el-color-primary);
}
.login-intro .desc {
	color: rgb(113, 115, 112);
	line-height: 32px;
	padding: 15px 0;
}
.login-bg img {
	width: 520px;
}
.login-form {
	//background-color: #fff;
	flex: 0 1 auto;
	padding: 40px;
	border-radius: 6px;
	box-shadow: 1px 1px 8px #aaa6a6;
	border: 1px solid #fff;
	box-sizing: border-box;
	width: 440px;

	:deep(.el-input) {
		height: 45px;
		margin-top: 5px;
		.el-input__inner {
			padding: 10px 15px 10px 5px;
			height: 45px;
			line-height: 45px;
			color: #666;
			font-size: 16px;
		}
	}
}

.login-more {
	display: flex;
	justify-content: space-evenly;
	padding-top: 25px;
	width: 200px;
	margin: 0 auto;
}
@media only screen and (max-width: 992px) {
	.login-intro {
		display: none;
	}
}
@media only screen and (max-width: 768px) {
	.login-container {
		background: #fff;
	}
	.login-intro {
		display: none;
	}
	.login-form {
		flex: 0 1 auto;
		border-radius: 0;
		box-shadow: none;
	}
	.login-captcha {
		:deep(.el-input) {
			width: 150px;
		}
	}
}
</style>
