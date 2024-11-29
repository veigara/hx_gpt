<template>
	<el-dialog v-model="visible" title="智能体" :close-on-click-modal="false">
		<template #title>
			<div class="header-title">智能体</div>
			<div>32个预设角色定义</div>
		</template>
		<el-row :gutter="20">
			<el-col :span="16">
				<el-input v-model="search" placeholder="搜索智能体"></el-input>
			</el-col>
			<el-col :span="8">
				<el-button title="新建" color="#567bff" @click="handleAdd">
					<template #icon>
						<svg-icon icon="icon-add"></svg-icon>
					</template>
					新建
				</el-button>
			</el-col>
		</el-row>
		<div class="agent">
			<div v-for="item in agentList" :key="item.id" class="agent_item">
				<div class="agent_header">
					<div class="agent_icon"></div>
					<div>
						<div class="agent_title">{{ item.title }}</div>
						<div class="agent_info">{{ item.title }}</div>
					</div>
				</div>
				<div class="agent_action">
					<el-button title="选择" color="#E6A23C" text>
						<template #icon>
							<svg-icon icon="icon-select"></svg-icon>
						</template>
						选择
					</el-button>
					<el-button title="查看" color="#E6A23C" text @click="handview(item)">
						<template #icon>
							<svg-icon icon="icon-view"></svg-icon>
						</template>
						查看
					</el-button>
				</div>
			</div>
		</div>
		<agent-add ref="agentAddRef"></agent-add>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus/es'
import AgentAdd from '@/views/chat/agentAdd.vue'
import { useUserAgentApi } from '@/api/chat'

const visible = ref(false)
const agentAddRef = ref()

interface agentContent {
	role: string
	chatText: string
}

interface modelConfig {
	modelName: string
	temperature: number
	top_p: number
	max_tokens: number
	presence_penalty: number
	frequency_penalty: number
}

interface agentModel {
	title: string
	content: [agentContent]
	modelConfig: modelConfig
}

const search = ref('')

const agentList = ref([])

// 获取当前用户所有智能体
const getAllAgent = () => {
	useUserAgentApi().then(res => {
		agentList.value = res
	})
}

const init = () => {
	visible.value = true
}

const handleAdd = () => {
	agentAddRef.value.init()
}

const handview = (item: agentModel) => {}
defineExpose({
	init
})

onMounted(() => {
	getAllAgent()
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
