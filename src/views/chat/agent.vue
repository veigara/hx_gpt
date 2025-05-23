<template>
	<el-dialog v-model="visible" title="角色体" :close-on-click-modal="false">
		<template #header>
			<div class="header-title">角色体</div>
			<div>{{ agentList.length }}个预设定义</div>
		</template>
		<el-row :gutter="isMobile()?2:20" justify="space-around">
			<el-col :xs="14" :sm="16" :md="16" :lg="16" :xl="16">
				<el-input v-model="search" placeholder="搜索角色体" @input="debouncedSearchTitle"></el-input>
			</el-col>
			<el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
				<div style="display:flex; flex-wrap: nowrap;">
					<el-button :icon="Search" circle @click="debouncedSearchTitle" />
				<el-button title="新建" color="#567bff" @click="handleAdd">
					<template #icon>
						<svg-icon icon="icon-add"></svg-icon>
					</template>
					新建
				</el-button>
				</div>
				
			</el-col>
		</el-row>
		<div class="agent">
			<div v-for="item in agentList" :key="item.id" class="agent_item">
				<div class="agent_header">
					<div class="agent_icon"></div>
					<div>
						<div class="agent_title">{{ item.title }}</div>
						<div class="agent_info">包含{{ item.count }}预设对话 / {{ item.model_name }}</div>
					</div>
				</div>
				<div class="agent_action">
					<el-button title="选择" type="success" text @click="selectview(item)">
						<template #icon>
							<svg-icon icon="icon-select"></svg-icon>
						</template>
						选择
					</el-button>
					<el-button title="查看" type="info" text @click="handview(item)">
						<template #icon>
							<svg-icon icon="icon-view"></svg-icon>
						</template>
						查看
					</el-button>
					<el-button title="删除" :icon="Delete" type="danger" text @click="delview(item)" v-if="item.edit">
						删除
					</el-button>
				</div>
			</div>
		</div>
		<agent-add ref="agentAddRef" @submit="getAllAgent(undefined)"></agent-add>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus/es'
import { Delete,Search } from '@element-plus/icons-vue'
import AgentAdd from '@/views/chat/agentAdd.vue'
import { useUserAgentApi, useAgentDetailApi, useDelAgentApi, useSelectAgentApi } from '@/api/chat'
import { debounce } from 'lodash';
import { isMobile } from '@/utils/tool'

const visible = ref(false)
const agentAddRef = ref()

interface agentContent {
	role: string
	chatText: string
}

interface modelConfig {
	model_name: string
	temperature: number
	top_p: number
	max_tokens: number
	presence_penalty: number
	frequency_penalty: number
}

interface agentModel {
	id: string,
	title: string
	content: [agentContent]
	modelConfig: modelConfig,
	edit: boolean
	user_name: string,
	model_name: string
}

const search = ref('')

const agentList = ref([])

const emit = defineEmits(['submit'])

// 获取当前用户所有角色体
const getAllAgent = (title:string) => {
	const params = title || title !='' ? { keyword: title } : {};
	useUserAgentApi(params).then(res => {
		agentList.value = res.data
	})

}

const init = () => {
	visible.value = true
	search.value = ''
	getAllAgent('')
}

const handleAdd = () => {
	clearAgentAdd()
}

const clearAgentAdd = () => {
	const data = {
		id: '',
		title: '',
		content: [],
		model_name: '',
		model_key: '',
		temperature: 0.5,
		top_p: 0.2,
		max_tokens: 8000,
		presence_penalty: 0,
		frequency_penalty: 0,
		user_icon:'',
		assistant_icon:''
	}
	agentAddRef.value.init(data, true)
}
/**
 * 查看角色体详情
 * @param item 
 */
const handview = (item: agentModel) => {
	// 先清空
	clearAgentAdd()
	useAgentDetailApi({ "id": item.id }).then(res => {
		agentAddRef.value.init(res.data, item.edit)
	})
}

/**
 * 搜索角色体
 */
const searchTitle = () => {
	getAllAgent(search.value)
}

// 300ms 的防抖时间
const debouncedSearchTitle = debounce(searchTitle, 300);

// 删除
const delview = (item: agentModel) => {
	ElMessageBox.confirm(
		'是否确认删除该角色体？',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			useDelAgentApi({ "id": item.id }).then(res => {
				ElMessage.success('删除成功')
				// 刷新列表
				getAllAgent(undefined)
			})
		})
}

// 选择角色体
const selectview = (item: agentModel) => {
	useSelectAgentApi({ "id": item.id, "fileUserName": item.user_name }).then(res => {
		const historyId = res
		// 关闭角色体
		visible.value = false
		// 提交选择
		emit('submit', historyId)
	})

}

defineExpose({
	init
})

onMounted(() => {
	getAllAgent('')
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

.agent {
	padding: 20px 0px;
}

.agent_item {
	display: flex;
	justify-content: space-between;
	padding: 20px;
	border: 1px solid #dedede;
	flex-wrap: wrap;
}

.agent_item:not(:last-child) {
	border-bottom: 0px;
}

.agent_item:first-child {
	border-top-left-radius: 10px;
	border-top-right-radius: 10px;
}

.agent_item:last-child {
	border-bottom-left-radius: 10px;
	border-bottom-right-radius: 10px;
}

.agent_header {
	display: flex;
	align-items: center;

	.agent_icon {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 10px;
	}

	.agent_title {
		font-size: 14px;
		font-weight: 700;
	}

	.agent_info {
		font-size: 12px;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
}

.agent_action {
	display: flex;
	flex-wrap: nowrap;
}
</style>
