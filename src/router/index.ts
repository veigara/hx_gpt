import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

export const menuRoutes: RouteRecordRaw[] = [
	{
		path: '/gen/generator',
		name: 'Generator',
		component: () => import('../views/generator/index.vue'),
		meta: {
			title: '对话',
			icon: 'icon-wechat-fill'
		}
	}
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
		redirect: '/gen/generator',
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
