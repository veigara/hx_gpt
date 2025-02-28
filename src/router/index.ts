import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import store from '@/store'
import { isMobile } from '@/utils/tool'

export const menuRoutes: RouteRecordRaw[] = [
	{
		path: '/chat',
		name: 'Chat',
		component: () => import('../views/chat/index.vue'),
		meta: {
			title: '对话',
			icon: 'icon-wechat-fill'
		},
	},
	{
		path: '/model',
		name: 'Model',
		component: () => import('../views/model/index.vue'),
		meta: {
			title: '模型',
			icon: 'icon-fire'
		}
	},
	{
		path: '/knowledge',
		name: 'Knowledge',
		component: () => import('../views/knowledge/index.vue'),
		meta: {
			title: '知识库',
			icon: 'icon-sketch'
		}
	},
]

export const constantRoutes: RouteRecordRaw[] = [
	// 手机页面
	{
		path: '/chat_mobile',
		name: 'ChatMobile',
		component: () => import('../views/chat/index.vue'),
		meta: {
			title: '对话',
			hidden: true  // 添加隐藏标识
		}
	},
	{
		path: '/redirect',
		component: () => import('../layout/index.vue'),
		children: [
			{
				path: '/redirect/:path(.*)',
				component: () => import('../layout/components/Router/Redirect.vue')
			}
		]
	},
	{
		path: '/',
		component: () => import('../layout/index.vue'),
		redirect: '/chat',
		children: [...menuRoutes]
	},
	{
		path: '/404',
		component: () => import('../views/404.vue')
	},
	{
		path: '/:pathMatch(.*)',
		redirect: '/404'
	},
	{
		path: '/login',
		component: () => import('../views/login/index.vue')
	},
]

export const router = createRouter({
	history: createWebHashHistory(),
	routes: constantRoutes
})

// 白名单列表
const whiteList = ['/login']

// 路由跳转前
router.beforeEach(async (to, from, next) => {
	NProgress.start()
	// token存在的情况
	if (store.userStore?.token) {
		if (to.path === '/login') {
			if(!isMobile()){
				next('/chat')
			}else{
				// 手机端
				next('/chat_mobile')
			}			
		} else {
			next()
		}
	} else {
		// 没有token的情况下，可以进入白名单
		if (whiteList.indexOf(to.path) > -1) {
			next()
		} else {
			next('/login')
		}
	}
})

// 路由加载后
router.afterEach(() => {
	NProgress.done()
})