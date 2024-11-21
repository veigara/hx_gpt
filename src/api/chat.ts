import service from '@/utils/request'

export const useChatApi = (dataForm: any) => {
	return service.get('/chat' ,{params: dataForm})
}

