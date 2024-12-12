<template>
	<div class="chat_main_plane">
		<div class="chat_main_plane_icon">
			<!--上传-->
			<div class="chat_main_plane_space">
				<el-popover placement="top" trigger="hover" :show-arrow="false">
					<template #reference>
						<el-button title="上传" round>
							<template #icon>
								<svg-icon icon="icon-upload"></svg-icon>
							</template>
						</el-button>
					</template>
					<div class="history-menu">
						<el-tooltip effect="light" content="支持PDF、World、Execl,最大100M" placement="right" :offset="-5">
							<div class="history-menu-item">
								<span><svg-icon icon="icon-upload-flie" /></span>上传文档
							</div>
						</el-tooltip>
						<el-tooltip effect="light" content="上传1张不超过10M的PNG/JPG的图片" placement="right" :offset="-5">
							<div class="history-menu-item" style="color: #181818 !important; border-top: none ;">
								<span><svg-icon icon="icon-upload-image" /></span>上传图片
							</div>
						</el-tooltip>
					</div>
				</el-popover>
			</div>
			<!--模型-->
			<div class="chat_main_plane_space">
				<el-popover placement="top" trigger="hover" :show-arrow="false">
					<template #reference>
						<el-button title="大模型" round>
							<template #icon>
								<svg-icon icon="icon-Checkpoint"></svg-icon>
							</template>
						</el-button>
					</template>
					<mode-select v-model="curModel" style="width: 120px;" />
				</el-popover>

			</div>
			<!--智能体-->
			<div class="chat_main_plane_space">
				<el-button title="智能体" round @click="showAgentVisible">
					<template #icon>
						<svg-icon icon="icon-agent"></svg-icon>
					</template>
				</el-button>
			</div>
			<!--连续对话-->
			<div class="chat_main_plane_space">
				<el-popover placement="top" trigger="hover" :show-arrow="false">
					<template #reference>
						<el-button title="连续对话" round>
							<template #icon>
								<svg-icon icon="icon-conv" :size="18"></svg-icon>
							</template>
						</el-button>
					</template>
					连续对话：<el-switch v-model="convOff"
						style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
				</el-popover>
			</div>
			<!--在线搜索-->
			<div class="chat_main_plane_space">
				<el-popover placement="top" trigger="hover" :show-arrow="false">
					<template #reference>
						<el-button title="在线搜索" round>
							<template #icon>
								<svg-icon icon="icon-search-online" :size="15"></svg-icon>
							</template>
						</el-button>
					</template>
					在线搜索：<el-switch v-model="searchOnline"
						style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
				</el-popover>
			</div>

		</div>
		<!--发送框-->
		<div class="chat_main_plane_label">
			<el-scrollbar :max-height="100" style="width: 100%;">
				<div class="chat_textarea">
					<el-input v-model="chatBotMst" :autosize="{ minRows: 2 }" type="textarea"
						input-style="height: 100%;width: 100%;border-radius: 10px;border: none;box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.00);background-color: white;color: black;font-family: inherit;padding: 10px 30px 10px 14px;resize: none;outline: none;box-sizing: border-box;resize:none !important;overflow: hidden;"
						placeholder="Enter 发送，Shift + Enter 换行" @keyup.enter="sendBotMsgClick">
					</el-input>
				</div>
			</el-scrollbar>
			<div class="chat_input_send">
				<el-button color="#ff0000" disabled v-if="chatData?.isLoading">加载中</el-button>
				<el-button color="#626aef" @click="sendBotMsgClick" v-else>
					<div style="margin-right: 5px;">
						<svg-icon icon="icon-send_right" />
					</div>
					发送
				</el-button>

			</div>

		</div>
		<Agent ref="agentRef" @submit="useSelectAgentApi" />
	</div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, onUpdated, computed, watch } from 'vue'
import { ElNotification } from 'element-plus/es'
import { useModelsApi, useChatApi } from '@/api/chat'
import Agent from '@/views/chat/agent.vue'
import ModeSelect from '@/components/model-select/index.vue'

interface Props {
	// 错误弹框
	ElNotificationErr: Function,
	historyId: string,
	agentId: string,
	// 重新发送的内容
	sendContent: string
}

//正在对话
interface chatBot {
	// 用户输入
	userCt: string,
	// 机器人回复
	assistantCt: string,
	// 是否正在回复
	isLoading: boolean
}

const props = defineProps<Props>()
// 当前模型
const curModel = ref()
// 正在进行的对话数据
const chatData = reactive({
	userCt: '',
	assistantCt: '',
	isLoading: false
})
// 对话输入框的数据
const chatBotMst = ref('')
// 智能体显示弹窗
const agentVisible = ref(false)
const agentRef = ref()

// 连续对话开关显示
const convOff = ref(true)
// 在线搜索显示
const searchOnline = ref(false)

const mounted = onMounted(() => {
	// 获取所有的模型
	getModelList();
});

// 定义事件，方便传值
const emit = defineEmits(['update:chatBotDataUser', 'update:chatBotDatAssert', 'update:curModel', "update:selectAgent"])

// 监听 chatBotMst 的变化
watch(curModel, (newVal, oldVal) => {
	emit('update:curModel', newVal)
})

// 获取所有的模型
const getModelList = () => {
	useModelsApi().then(res => {
		res.filter(item => item.default == true).forEach(model => {
			// 获取默认的模型
			curModel.value = model.label
		})
	})
}

// 发送按钮
const sendBotMsgClick = (event: any) => {
	if (event.shiftKey) {
		//shift+enter 不触发此事件
		return
	}
	// 获取输入框的内容并去除换行符
	const message = chatBotMst.value.trim();
	if (!message) {
		ElNotification({
			title: '提示',
			message: '请输入要咨询的问题',
			type: 'warning'
		})
		return
	}
	const curMsg = {
		userCt: message,
		assistantCt: '',
		isLoading: true
	}
	chatData.userCt = message
	chatData.isLoading = true
	// 传输数据
	emit('update:chatBotDataUser', curMsg)
	// 对话
	const data = {
		input_text: message,
		model_name: curModel.value,
		history_id: props.historyId,
		agent_id: props.agentId,
		conv_off: convOff.value
	}
	useChatApi(data).then(res => {
		chatData.assistantCt = res
		chatData.isLoading = false
		// 将更新后的数据传递给父组件
		emit('update:chatBotDatAssert', chatData)
	}).catch(err => {
		chatData.isLoading = false
		emit('update:chatBotDatAssert', chatData)
	})
	// 清空发送的消息
	chatBotMst.value = ''
}

// 展示智能体弹窗
const showAgentVisible = () => {
	agentRef.value.init()
}

// 向父组件传递选择的智能体
const useSelectAgentApi = (historyId: string) => {
	emit('update:selectAgent', historyId)
}

// 初始化发送框
const init = (modelName: string) => {
	chatData.assistantCt = ''
	chatData.userCt = ''
	chatData.isLoading = false
	// 对话输入框的数据
	chatBotMst.value = ''
	// 智能体显示弹窗
	agentVisible.value = false
	curModel.value = modelName
}

watch(() => props.sendContent, (newVal, oldVal) => {
	if (newVal) {
		chatBotMst.value = newVal
		sendBotMsgClick({})
	}
})

defineExpose({
	init
})	
</script>
<style lang="scss">
.chat_main_plane {
	height: 115px;
	border-top: 1px solid #ebeef5;
	padding: 10px;
	padding-top: 10px;
	max-width: 1150px;
	margin: 16px auto;
}

.chat_main_plane_icon {
	display: flex;
	flex-wrap: wrap;
	flex-direction: row;

	.chat_main_plane_space {
		margin-right: 10px;
	}
}

.chat_main_plane_label {
	margin-top: 10px !important;
	cursor: text;
	border-radius: 15px;
	border: 1.2px solid #ebeef5;
	align-items: flex-end;
	display: flex;
	flex: 1;
	margin: 0 auto;
	overflow: auto;
	position: relative;
	width: 100%;
	z-index: 2;
	background-color: white;
}


.chat_main_plane_label:has(.el-textarea__inner:focus) {
	border: 1px solid #626aef;
}

.chat_textarea {
	height: 100%;
	position: relative;
	width: calc(100% - 50px)
}

.chat_input_send {
	align-items: center;
	bottom: 7px;
	color: #fff;
	cursor: pointer;
	display: flex;
	flex-shrink: 0;
	justify-content: center;
	position: absolute;
	right: 7px;
}
</style>
