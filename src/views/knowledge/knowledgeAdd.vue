<template>
	<el-dialog v-model="visible" :title="!dataForm.id ? '新增知识库' : '修改知识库'" :close-on-click-modal="false" append-to-body>
		<el-form ref="dataFormRef" :model="dataForm" label-width="auto" label-position="left" :rules="rules">
			<el-collapse v-model="activeNames">
				<el-collapse-item title="Consistency" name="1">
					<template #title>
						<div style="font-size: 16px;"><svg-icon icon="icon-wrench" style="display: inline-block;" />基本配置
						</div>
					</template>
					<div class="know-config">
						<el-form-item label="知识库名称" prop="know_name">
							<el-input v-model="dataForm.know_name" placeholder="请输入知识库名称"
								:disabled="editFlag"></el-input>
						</el-form-item>
						<el-form-item label="索引名称(英文)" prop="index_name" >
							<el-input v-model="dataForm.index_name" placeholder="请输入索引名称"
								:disabled="dataForm.id"></el-input>
						</el-form-item>
						<el-form-item label="描述" prop="description">
							<el-input :autosize="{ minRows: 2 }" type="textarea" v-model="dataForm.description"
								placeholder="请输入描述"></el-input>
						</el-form-item>
						<div style="display: flex;justify-content: center;">
							<el-button type="primary" @click="saveUpdate">提交</el-button>
						</div>
					</div>
				</el-collapse-item>
				<el-collapse-item title="Consistency" name="2">
					<template #title>
						<div style="font-size: 16px;"><svg-icon icon="icon-cloud-upload"
								style="display: inline-block;" />添加文件到知识库</div>
					</template>
					<div class="know-config">
						<el-upload class="upload-demo" drag :http-request="upload" multiple
							accept=".html,.htm,.mhtml,.md,.json,.jsonl,.csv,.pdf,.docx,.ppt,.pptx,.png,.jpg,.jpeg,.bmp,.eml,.msg,.rst,.rtf,.txt,.xml,.epub,.odt,.tsv,.xlsx,.xls,.xlsd,.ipynb,.py,.srt,.toml,.enex"
							show-file-list :file-list="fileList" :on-change="handleFileChanged">
							<i class="el-icon-upload"></i>
							<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
							<div class="el-upload__tip" slot="tip">上传文件且不超过200M</div>
						</el-upload>
					</div>
				</el-collapse-item>
				<el-collapse-item title="Consistency" name="3">
					<template #title>
						<div style="font-size: 16px;"><svg-icon icon="icon-filesearch" style="display: inline-block;" />
							<span>知识库已有文件</span>
						</div>
					</template>
					<div class="know-config">
						<el-row :gutter="20" style="margin-bottom: 5px;">
							<el-col :span="16">
								<el-input v-model="knowSearch" placeholder="请输入文件名称" clearable />
							</el-col>
							<el-col :span="8">
								<el-button type="primary" @click="search_file">搜索</el-button>
							</el-col>
						</el-row>
						<el-table :data="knowFileList" stripe style="width: 100%" max-height="250" border
							class="center-table">
							<el-table-column prop="title" label="文件名" show-overflow-tooltip />
							<el-table-column prop="file_type" label="文件类型" width="90">
								<template #default="scope">
									<el-tag type="primary">{{ scope.row.file_type }}</el-tag>
								</template>
							</el-table-column>
							<el-table-column prop="file_size" label="文件大小(兆)" width="110" />
							<el-table-column prop="file_index_name" label="索引名称" width="120" />
							<el-table-column prop="create_time" label="创建时间" width="170" />
							<el-table-column fixed="right" label="操作" width="100">
								<template #default="scope">
									<el-button link type="danger" size="small"
										@click="delFile(scope.row.id)">删除</el-button>
								</template>
							</el-table-column>
						</el-table>
					</div>
				</el-collapse-item>
			</el-collapse>

		</el-form>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { ElNotification,ElMessageBox } from 'element-plus'
import { useKnowledgeFileUploadApi, useKnowledgeFileSearchApi, useKnowledgeFileDelApi,useKnowledgeSaveUpdateApi,} from '@/api/knowledge'

const visible = ref(false)

const dataFormRef = ref()

const emit = defineEmits(['submit'])

const dataFormData = {
	id: undefined,
	know_name: '',
	index_name: '',
	description: ''
}

const dataForm = reactive({ ...dataFormData })

const editFlag = ref(false)
// 折叠面板
const activeNames = ref(['1'])
// 上传的文件
const fileList = ref([])
// 文件
const knowFileList = ref()
// 知识库搜索
const knowSearch = ref()

// 初始化
const init = (data?: any) => {
	visible.value = true
	Object.assign(dataForm, dataFormData)
	if (data) {
		Object.assign(dataForm, data)
		search_file()
	}
}

// 上传文件
const upload = (data: any) => {
	if (!dataForm.id) {
		ElMessageBox.alert('请先保存知识库', '提示', {
			confirmButtonText: '确定',
			type: 'warning',
		})
		return false
	}
	const formData = new FormData();
	formData.append('file', data.file);
	formData.append('id', dataForm.id);
	// 检查是否有重复文件，有的话删除新选择的文件
	const file = data.file
	const fileData = fileList.value.find(f => f.name === file.name)
	if (fileData) {

		return false
	}
	return useKnowledgeFileUploadApi(formData).then(res => {
		ElNotification({
			title: '温馨提示',
			message: '上传成功',
			type: 'success'
		})
		search_file()
	})
}

const handleFileChanged = (file: any, yfileList: any) => {
	const fileData = fileList.value.find(f => f.name === file.name)
	if (fileData) {
		ElNotification({
			title: '温馨提示',
			message: file.name + '文件已存在',
			type: 'warning'
		})
		yfileList.pop()
		return false
	}

	if (file.status == 'success') {
		fileList.value.push(file)
	}


}

// 查询上传文件
const search_file = () => {
	const query = {
		knowledge_id: dataForm.id,
		title: knowSearch.value
	}
	useKnowledgeFileSearchApi(query).then(res => {
		knowFileList.value = res.data
	})
}

// 删除文件
const delFile = (id: string) => {
	const query = {
		id: id
	}
	ElMessageBox.confirm(
		'是否确认删除该文件？删除后不可恢复',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		})
		.then(() => {
			useKnowledgeFileDelApi(query).then(res => {
				ElNotification({
					title: '温馨提示',
					message: '删除成功',
					type: 'success'
				})
				search_file()
			})
		})



}

// 搜索知识库索引
const searchKnowledgeIndex = () => {

}

// 更新/添加知识库
const saveUpdate = () => {
	const index_name = dataForm.index_name
	const data = {
		id: dataForm.id,
		know_name: dataForm.know_name,
		index_name: index_name,
		description: dataForm.description
	}
	// 验证索引只能是英文和下划线
	if (!/^[a-zA-Z0-9_]+$/.test(index_name)) {
		ElNotification({
			title: '温馨提示',
			message: '索引名称只能是英文和下划线',
			type: 'warning'
		})
		return false
	}

	
	useKnowledgeSaveUpdateApi(data).then(res => {
		let message = '保存成功'
		if(dataForm.id){
			message = '更新成功'
		}
		ElNotification({
			title: '温馨提示',
			message: message,
			type: 'success'
		})
		Object.assign(dataForm,res.data)
		emit('submit')
	})
}

const rules = reactive({
	know_name: [{ required: true, message: '知识库名称不能为空', trigger: 'blur' }],
	index_name: [
		{
			required: true,
			message: '索引名称不能为空',
			trigger: 'blur'
		}
	]	
})

// 更新
onMounted(() => {
	
})

defineExpose({
	init
})
</script>

<style lang="scss" scoped>
.header-title {
	font-size: 20px;
	font-weight: bolder;
	text-overflow: ellipsis;
	display: block;
	max-width: 50vw;
	overflow: hidden;
	white-space: nowrap;
}

.margin-top-20 {
	margin-top: 20px;
}

.margin-top-5 {
	margin-top: 5px;
}

.margin-top-10 {
	margin-top: 10px;
}

.know-config {
	margin-top: 5px;
	margin-bottom: 20px;
	padding: 10px;
	border: 1px solid rgb(0, 0, 0, 0.1);
	border-radius: 4px;
}

:deep(.center-table td),
:deep(.center-table th) {
	text-align: center !important;
}
</style>
