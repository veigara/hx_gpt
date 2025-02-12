import service from '@/utils/request'
import type { Ref } from 'vue'

export const useChatApi = (dataForm: any) => {
	return service.post('/chat' ,dataForm)
}

export const useModelsApi = () => {
	return service.get('/models')
}

export const useSaveAgentFileApi = (dataForm: any) => {
	return service.post('/save_agent_file' ,dataForm)
}

export const useUserAgentApi = (params: any) => {
	return service.get('/get_user_agent',{params})
}

export const useAgentDetailApi = (params: any) => {
	return service.get('/get_agent_detail',{params})
}

export const useDelAgentApi = (params: any) => {
	return service.delete('/del_agent',{params})
}

export const useSelectAgentApi = (params: any) => {
	return service.get('/select_agent',{params})
}

export const useGetHistorysApi = (params: any) => {
	return service.get('/get_historys',{params})
}

export const useGetHistoryDetailApi = (params: any) => {
	return service.get('/get_history_detail',{params})
}

export const useDelHistoryApi = (params: any) => {
	return service.delete('/del_history',{params})
}

export const useRenameHistoryApi = (params: any) => {
	return service.post('/rename_history',params)
}

export const useTopHistoryApi = (params: any) => {
	return service.post('/top_history',params)
}

export const useClearHistoryContextApi = (params: any) => {
	return service.post('/clear_history_context',params)
}

export const useClearHistoryAllApi = () => {
	return service.post('/clear_history_all')
}

export const useHistoryTokensApi = (params: any) => {
	return service.get('/get_count_tokens',{params})
}