import type { App, Plugin } from 'vue'
import MobileDetect from 'mobile-detect'
// 全局组件安装
export const withInstall = <T>(component: T, alias?: string) => {
	const comp = component as any
	comp.install = (app: App) => {
		app.component(comp.__name || comp.displayName, component)
		if (alias) {
			app.config.globalProperties[alias] = component
		}
	}
	return component as T & Plugin
}

// 获取svg图标(id)列表
export const getIconList = (suffx:string): string[] => {
	suffx = suffx || 'icon-'
	const rs: string[] = []
	const list = document.querySelectorAll('svg symbol[id^="'+suffx+'"]')
	for (let i = 0; i < list.length; i++) {
		rs.push(list[i].id)
	}
	return rs
}

// 是否是移动端
export const isMobile = (): boolean => {
	const md = new MobileDetect(window.navigator.userAgent)
	return md.mobile() ? true : false
}