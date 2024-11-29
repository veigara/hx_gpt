<template>
	<el-dialog v-model="visible" title="智能体" :close-on-click-modal="false">
		<template #title>
			<div class="header-title"> 智能体</div>
			<div> 32个预设角色定义</div>
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
		<el-row>
			<ul  class="infinite-list" style="overflow: auto">
				<li v-for="item in agentList" :key="item.id" class="infinite-list-item">{{ item.title }}</li>
			</ul>
		</el-row>
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
	role: string,
	chatText: string
}

interface modelConfig {
	modelName: string,
	temperature: number,
	top_p: number,
	max_tokens: number,
	presence_penalty: number,
	frequency_penalty: number
}

interface agentModel {
	title: string,
	content: [agentContent],
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
</style>
