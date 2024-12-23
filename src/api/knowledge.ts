import service from '@/utils/request'

// 上传文件
export const useKnowledgeUploadApi = (data:any) => {
	return service.post('/knowledge/upload',data,{headers:{'Content-Type':'multipart/form-data'}})
}