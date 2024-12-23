<template>
	<el-dialog v-model="visible" :title="!dataForm.id ? '新增智能体' : editFlag ? '修改智能体' : '查看智能体'" :close-on-click-modal="false"
		append-to-body>
		<el-form ref="dataFormRef" :model="dataForm" label-width="40%" label-position="left" :rules="rules"
			:disabled="!editFlag">
			<el-row type="flex" justify="center">
				<el-col :span="24">
					<el-button plain type="primary" icon="el-icon-plus" style="width: 100%" @click="addAgentContent()"
						v-if="editFlag">新增一条对话</el-button>
				</el-col>
			</el-row>
			<div v-for="(agentContent, index) in dataForm.content" :key="index">
				<el-row class="margin-top-20" :gutter="20">
					<el-col :span="4">
						<el-select v-model="agentContent.role" placeholder="请选择" :disabled="!editFlag">
							<el-option v-for="item in role" :key="item" :label="item" :value="item"> </el-option>
						</el-select>
					</el-col>
					<el-col :span="20">
						<el-input v-model="agentContent.content" type="textarea" :rows="1" placeholder="请输入内容"
							:disabled="!editFlag" :autosize="{ minRows: 1, maxRows: 4 }"> </el-input>
					</el-col>
				</el-row>
				<el-row class="margin-top-5" :gutter="20" type="flex" justify="center" v-if="editFlag">
					<el-col :span="6">
						<el-button v-if="index === dataForm.content.length - 1" type="primary" :icon="CirclePlus" circle
							title="添加" @click="addAgentContent()" />
						<el-button type="danger" :icon="Delete" circle title="删除" @click="removeAgentContent(index)" />
					</el-col>
				</el-row>
			</div>
			<div class="agengt-config">
				<el-form-item label="智能体名称" prop="title">
					<el-input v-model="dataForm.title" placeholder="智能体名称"></el-input>
				</el-form-item>
				<el-form-item label="用户图标" prop="user_icon">
					<icon-select v-model="dataForm.user_icon" suffx="icon-avatar-"/>
				</el-form-item>
				<el-form-item label="助理图标" prop="assistant_icon">
					<icon-select v-model="dataForm.assistant_icon" suffx=""/>
				</el-form-item>
				<el-form-item label="模型(model)" prop="model_name">
					<mode-select v-model="dataForm.model_name" style="width: 100%"/>
				</el-form-item>
				<el-form-item prop="temperature">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>随机性(temperature)</div>
							<div class="agent-label-small">值越大，回复越随机</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.temperature" show-input show-stops :max="1" :min="0" :step="0.1" />
					</div>
				</el-form-item>
				<el-form-item prop="top_p">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>核采样(top_p)</div>
							<div class="agent-label-small">与随机性类似，但不要和随机性一起更改</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.top_p" show-input show-stops :max="1.0" :min="0" :step="0.1" />
					</div>
				</el-form-item>
				<el-form-item prop="max_tokens">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>单次回复限制(max_tokens)</div>
							<div class="agent-label-small">单次交互所用的最大Token数</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.max_tokens" show-input :max="100000" :min="0" :step="1" />
					</div>
				</el-form-item>
				<el-form-item prop="presence_penalty">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>话题新鲜度(presence_penalty)</div>
							<div class="agent-label-small">值越大，越有可能扩展到新话题</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.presence_penalty" show-input show-stops :max="2.0" :min="0"
							:step="0.1" />
					</div>
				</el-form-item>
				<el-form-item prop="frequency_penalty">
					<template #label>
						<div style="display: flex; flex-direction: column">
							<div>频率惩罚度(frequency_penalty)</div>
							<div class="agent-label-small">值越大，越有可能降低重复字词</div>
						</div>
					</template>
					<div style="width: 100%">
						<el-slider v-model="dataForm.frequency_penalty" show-input show-stops :max="2.0" :min="0"
							:step="0.1" />
					</div>
				</el-form-item>
			</div>
		</el-form>
		<template #footer v-if="editFlag">
			<el-button @click="visible = false">取消</el-button>
			<el-button type="primary" @click="saveAgent">确定</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { useModelsApi, useSaveAgentFileApi } from '@/api/chat'
import { CirclePlus, Delete } from '@element-plus/icons-vue'
import IconSelect from '@/components/icon-select/src/index.vue'
import ModeSelect from '@/components/model-select/index.vue'

const visible = ref(false)

const dataFormRef = ref()

const emit = defineEmits(['submit'])

interface agentContent {
	role: string
	content: string
}

interface agentModel {
	id: string
	title: string
	content: agentContent[]
	model_name: string
	temperature: number
	top_p: number
	max_tokens: number
	presence_penalty: number
	frequency_penalty: number,
	user_icon:string,
	assistant_icon:string
}

const dataForm = reactive<agentModel>({
	id: '',
	title: '',
	content: [],
	model_name: '',
	temperature: 0.5,
	top_p: 0.2,
	max_tokens: 8000,
	presence_penalty: 0,
	frequency_penalty: 0,
	user_icon:'',
	assistant_icon:''
})

const role = ref(['user', 'system', 'assistant'])

const editFlag = ref(false)
// 初始化
const init = (data: agentModel, edit: boolean) => {
	visible.value = true
	if (data) {
		Object.assign(dataForm, data)
		editFlag.value = edit
	} else {
		clearForm()
	}
}

// 清空表单
const clearForm = () => {
	Object.assign(dataForm, {
		id: '',
		title: '',
		content: [],
		model_name: '',
		temperature: 0,
		top_p: 0,
		max_tokens: 0,
		presence_penalty: 0,
		frequency_penalty: 0,
		user_icon:'',
		assistant_icon:''
	})
}

const removeAgentContent = (index: number) => {
	dataForm.content.splice(index, 1)
}

const addAgentContent = () => {
	const agentContent = {
		role: '',
		content: ''
	}
	dataForm.content.push(agentContent)
}

const rules = reactive({
	title: [{ required: true, message: '智能体名称不能为空', trigger: 'blur' }],
	model_name: [
		{
			required: true,
			message: '请选择模型',
			trigger: 'change'
		}
	]
})

// 保存智能体
const saveAgent = () => {
	dataFormRef.value.validate(valid => {
		if (valid) {
			useSaveAgentFileApi({ agent_data: JSON.stringify(dataForm) }).then(res => {
				ElNotification({
					title: '温馨提示',
					message: '保存智能体成功',
					type: 'success'
				})
				// 关闭弹窗
				visible.value = false
				emit('submit')
				// 清空表单
				clearForm()
			})

		}
	})
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

.agengt-config {
	margin-top: 10px;
	padding: 10px;
	border: 1px solid rgb(0, 0, 0, 0.1);
	border-radius: 4px;
}

.agent-label-small {
	font-size: 0.8em;
	line-height: 2px;
}
</style>
