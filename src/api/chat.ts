import service from '@/utils/request'

export const useChatApi = (dataForm: any) => {
	return service.post('/chat' ,dataForm)
}

export const useModelsApi = () => {
	return service.get('/models')
}
