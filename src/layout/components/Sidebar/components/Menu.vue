<template>
	<el-scrollbar>
		<div class="sidebar-logo">
			<el-avatar :src="favicon"></el-avatar>
			<span class="logo-title">hx-gpt</span>
		</div>
		<el-menu :default-active="defaultActive" background-color="transparent" :collapse-transition="false"
			mode="vertical" router>
			<menu-item v-for="menu in menuRoutes" :key="menu.path" :menu="menu"></menu-item>
		</el-menu>
	</el-scrollbar>
</template>

<script setup lang="ts">
import MenuItem from './MenuItem.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { menuRoutes } from '@/router'
import favicon from '@/assets/favicon.ico' 

const route = useRoute()

const defaultActive = computed(() => {
	const { path } = route
	return path
})
</script>

<style lang="scss" scoped>
.sidebar-logo {
	line-height: var(--theme-header-height);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	box-shadow: rgb(0 21 41 / 2%) 0 1px 4px;
	color: var(--theme-logo-text-color);
	font-size: 18px;
	.el-avatar {
		width: 50px;
		height: 50px;
	}
	.logo-title {
		margin-left: 4px;
	}
	margin-bottom:48px
}
</style>
