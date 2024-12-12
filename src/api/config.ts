import service from '@/utils/request'

export const useGetConfigApi = () => {
	return service.get('/get_config')
}

export const useUpdateConfigApi = (data:any) => {
	return service.post('/update_config',data)
}