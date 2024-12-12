import service from '@/utils/request'

export const useModelTypeApi = () => {
	return service.get('/get_model_type')
}

export const useAllModelsApi = (params:any) => {
	return service.get('/get_all_models',{params})
}

export const useModelDetailApi = (params: any) => {
	return service.get('/get_model_detail',{params})
}

export const useRemoveModelApi = (params: any) => {
	return service.delete('/remove_model',{params})
}

export const useUpdateModelApi = (dataForm: any) => {
	return service.post('/update_model',dataForm)
}

export const useAddModelApi = (dataForm: any) => {
	return service.post('/add_model',dataForm)
}
