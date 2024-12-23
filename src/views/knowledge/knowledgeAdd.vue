<template>
	<el-dialog v-model="visible" :title="!editFlag ? '新增知识库' : '修改知识库'" :close-on-click-modal="false" append-to-body>
		<el-form ref="dataFormRef" :model="dataForm" label-width="auto" label-position="left">
			<div style="font-size: 16px;font-weight: bold;"><svg-icon icon="icon-wrench"
					style="display: inline-block;" />基本配置</div>
			<div class="know-config">
				<el-form-item label="知识库名称" prop="know_name">
					<el-input v-model="dataForm.know_name" placeholder="请输入知识库名称" :disabled="editFlag"></el-input>
				</el-form-item>
				<el-form-item label="描述" prop="description">
					<el-input :autosize="{ minRows: 2 }" type="textarea" v-model="dataForm.description"
						placeholder="请输入描述"></el-input>
				</el-form-item>
				<div style="display: flex;justify-content: center;">
					<el-button type="primary" @click="">提交</el-button>
				</div>
			</div>
			<div style="font-size: 16px;font-weight: bold;"><svg-icon icon="icon-file-add-fill"
					style="display: inline-block;" />添加文件到知识库</div>
			<div class="know-config">
				<el-upload class="upload-demo" drag :http-request="upload" multiple
					accept=".html,.htm,.mhtml,.md,.json,.jsonl,.csv,.pdf,.docx,.ppt,.pptx,.png,.jpg,.jpeg,.bmp,.eml,.msg,.rst,.rtf,.txt,.xml,.epub,.odt,.tsv,.xlsx,.xls,.xlsd,.ipynb,.py,.srt,.toml,.enex"
					show-file-list :file-list="fileList" :on-change="handleFileChanged">
					<i class="el-icon-upload"></i>
					<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
					<div class="el-upload__tip" slot="tip">上传文件且不超过200M</div>
				</el-upload>
			</div>
			<div style="font-size: 16px;font-weight: bold;"><svg-icon icon="icon-folder-open"
					style="display: inline-block;" />知识库已有文件</div>
			<div class="know-config">

			</div>
		</el-form>
		<!-- <template #footer>
			<el-button @click="visible = false">取消</el-button>
			<el-button type="primary" @click="">确定</el-button>
		</template> -->
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { de, id } from 'element-plus/es/locale';
import { useKnowledgeUploadApi } from '@/api/knowledge'
import { file } from '@babel/types';

const visible = ref(false)

const dataFormRef = ref()

const emit = defineEmits(['submit'])

const dataFormData = {
	id: '',
	know_name: '',
	description: ''
}

const dataForm = reactive({ ...dataFormData })

const editFlag = ref(false)
// 上传的文件
const fileList = ref([])
// 初始化
const init = (data?: any) => {
	visible.value = true
	Object.assign(dataForm, dataFormData)
	if (data) {
		Object.assign(dataForm, data)
	}
}

const upload = (data: any) => {
	const formData = new FormData();
	formData.append('file', data.file);
	formData.append('id', "123");
	// 检查是否有重复文件，有的话删除新选择的文件
	const file = data.file
	const fileData = fileList.value.find(f => f.name === file.name) 
	if (fileData) {

		return false
	}    
	return useKnowledgeUploadApi(formData).then(res => {
		ElNotification({
			title: '温馨提示',
			message: '上传成功',
			type: 'success'
		})
	})
}

const handleFileChanged = (file: any, yfileList: any) => {
	const fileData = fileList.value.find(f => f.name === file.name) 
	if (fileData) {
		ElNotification({
			title: '温馨提示',
			message: file.name+'文件已存在',
			type: 'warning'
		})
		yfileList.pop()
		return false
	}  
	
	if(file.status == 'success'){
		fileList.value.push(file)
	}
	

}
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
</style>
