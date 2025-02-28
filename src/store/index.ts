import { userStore } from './modules/user'

const store: any = {}

export const registerStore = () => {
	store.userStore = userStore()
}

export default store
