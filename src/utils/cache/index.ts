import { Storage } from '@/utils/storage'
import CacheKey from '@/utils/cache/key'

// 缓存
class Cache {
	getToken = (): string => {
		return Storage.getItem(CacheKey.TokenKey) || ''
	}

	setToken = (value: string) => {
		Storage.setItem(CacheKey.TokenKey, value)
	}
}

export default new Cache()
