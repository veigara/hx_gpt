import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

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
	}
]

export const router = createRouter({
	history: createWebHashHistory(),
	routes: constantRoutes
})
