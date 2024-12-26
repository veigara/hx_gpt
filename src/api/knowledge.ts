import service from '@/utils/request'

// 上传文件
export const useKnowledgeFileUploadApi = (data:any) => {
	return service.post('/knowledge_file/upload',data,{headers:{'Content-Type':'multipart/form-data'}})
}

// 查询文件
export const useKnowledgeFileSearchApi = (params:any) => {
	return service.get('/knowledge_file/search',{params})
}

// 删除文件
export const useKnowledgeFileDelApi = (params:any) => {
	return service.delete('/knowledge_file/delete',{params})
}

// 保存/更新知识库基本信息
export const useKnowledgeSaveUpdateApi = (data:any) => {
	return service.post('/knowledge/save_update',data)
}

// 搜索知识库基本信息
export const useKnowledgeSearchApi = (params:any) => {
	return service.get('/knowledge/search',{params})
}

// 删除知识库基本信息
export const useKnowledgeDelApi = (params:any) => {
	return service.delete('/knowledge/delete',{params})
}