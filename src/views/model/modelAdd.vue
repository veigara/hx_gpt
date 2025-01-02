<template>
	<el-dialog v-model="visible" :title="!editFlag ? '新增模型' : '修改模型'" :close-on-click-modal="false" append-to-body>
		<el-form ref="dataFormRef" :model="dataForm" label-width="auto" label-position="left" :rules="rules">
			<div class="model-config">
				<el-form-item label="模型显示名称" prop="model_name">
					<el-input v-model="dataForm.model_name" placeholder="请输入模型显示名称"  clearable></el-input>
				</el-form-item>
				<el-form-item label="模型" prop="model_key">
					<el-input v-model="dataForm.model_key" placeholder="请输入模型名称" :disabled="editFlag" clearable></el-input>
				</el-form-item>

				<el-form-item label="模型类型" prop="model_type">
					<el-select v-model="dataForm.model_type" :teleported="false" placeholder="请选择模型类型"
						style="width: 100%">
						<el-option v-for="item in modelTypeList" :key="item" :label="item" :value="item">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="多态" prop="multimodal">
					<el-select v-model="dataForm.multimodal" :teleported="false" placeholder="请选择" style="width: 100%">
						<el-option v-for="item in multimodalList" :key="item.value" :label="item.label"
							:value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item prop="max_content_len" label="上下文长度">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>上下文长度</div>
							<div class="model-label-small">历史最大token,超出将自动清空历史对话</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.max_content_len" show-input :max="128 * 1024" :min="0" />
					</div>
				</el-form-item>
				<el-form-item label="模型描述" prop="description">
					<el-input :autosize="{ minRows: 2 }" type="textarea" v-model="dataForm.description"
						placeholder="请输入模型描述"></el-input>
				</el-form-item>

			</div>
		</el-form>
		<template #footer>
			<el-button @click="visible = false">取消</el-button>
			<el-button type="primary" @click="saveModel">确定</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { useModelTypeApi, useAddModelApi, useUpdateModelApi } from '@/api/model'

const visible = ref(false)

const dataFormRef = ref()

const emit = defineEmits(['submit'])

const dataFormData = {
	id: undefined,
	model_key: '',
	model_name: '',
	description: '',
	model_type: '',
	multimodal: false,
	max_content_len: 0
}

const dataForm = reactive({ ...dataFormData })

const editFlag = ref(false)
// 初始化
const init = (flag: boolean, data?: any) => {
	visible.value = true
	editFlag.value = flag
	Object.assign(dataForm, dataFormData)
	if (data) {
		Object.assign(dataForm, data)
	}
}

// 获取所有的模型类别
const modelTypeList = ref()
const getModelTypeList = () => {
	useModelTypeApi().then(res => {
		modelTypeList.value = res.data
	})
}

const multimodalList = [{
	label: '是',
	value: true
}, {
	label: '否',
	value: false
}
]

const rules = reactive({
	model_key: [{ required: true, message: '模型显示名称不能为空', trigger: 'blur' }],
	model_name: [
		{
			required: true,
			message: '模型名称不能为空',
			trigger: 'blur'
		}
	],
	model_type: [
		{
			required: true,
			message: '请选择模型类别',
			trigger: 'change'
		}
	],
	max_content_len: [
		{
			required: true,
			message: '上下文长度不能为空',
			trigger: 'change'
		}
	],

})

// 保存模型
const saveModel = () => {
	dataFormRef.value.validate(valid => {
		if (valid) {
			const sData = {
				"model_key": dataForm.model_key,
				"data": dataForm
			}
			if (editFlag.value) {
				useUpdateModelApi(sData).then(res => {
					ElNotification({
						title: '温馨提示',
						message: '修改模型成功',
						type: 'success'
					})
					emit('submit')
					// 关闭弹窗
					visible.value = false
				})

			} else {
				useAddModelApi(sData).then(res => {
					ElNotification({
						title: '温馨提示',
						message: '添加模型成功',
						type: 'success'
					})
					emit('submit')
					// 关闭弹窗
					visible.value = false
				})

			}
		}
	})
}

const mounted = onMounted(() => {
	// 获取所有的模型类型
	getModelTypeList()
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

.model-config {
	margin-top: 10px;
	padding: 10px;
	border: 1px solid rgb(0, 0, 0, 0.1);
	border-radius: 4px;
}

.model-label-small {
	font-size: 0.8em;
	line-height: 2px;
}
</style>
