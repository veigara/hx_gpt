import service from '@/utils/request'

export const useUserLoginApi = (dataForm: any) => {
	return service.post('/chat/login',dataForm)
}

export const useUserRegisterApi = (dataForm: any) => {
	return service.post('/chat/register',dataForm)
}
