import service from '@/utils/request'

export const useChatApi = (dataForm: any) => {
	return service.post('/chat' ,dataForm)
}

export const useModelsApi = () => {
	return service.get('/models')
}

export const useSaveAgentFileApi = (dataForm: any) => {
	return service.post('/save_agent_file' ,dataForm)
}

export const useUserAgentApi = () => {
	return service.get('/get_user_agent')
}

export const useagentDetailApi = (params: any) => {
	return service.get('/get_agent_detail',params)
}