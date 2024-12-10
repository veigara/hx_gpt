<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="300px" class="chat_card_aside" v-if="chatHistoryDisplay">
				<HistoryAside ref="historyRef" @click:history="item => selectHistoryItem(item)" @refresh:history="refreshHistory"/>
			</el-aside>

			<el-main class="chat_card_main">
				<div class="chat_history_expend" @click="chatHistoryDisplay = !chatHistoryDisplay">
					<svg-icon icon="icon-arrow-expand" v-if="!chatHistoryDisplay"></svg-icon>
					<svg-icon icon="icon-arrow-fold" v-if="chatHistoryDisplay"></svg-icon>
				</div>
				<!--头部-->
				<div style="height: 40px;border-bottom: 1px solid #ebeef5;">
					<el-row style="padding: 0px 20px;">
						<el-col :span="16">
							模型名称: <span style="color: #00BFFF;">{{ curModel }}</span>
						</el-col>
						<el-col :span="8" style="display: flex;justify-content: end;">
							<span style="color: #a6a6a6;">本次对话累计消耗了 {{curAgent.token_count }} tokens</span>	
						</el-col>
					</el-row>
					<el-row style="padding: 0px 20px;">
						<el-col :span="16">
							智能体: <span style="color: #00BFFF;">{{ curAgent.agent_title }}</span>
						</el-col>
					</el-row>
				</div>
				<!--内容-->
				<div style="height: calc(100vh - 270px);">
					<el-scrollbar max-height="100%" style="width: 100%;" ref="scrollbarRef">
						<div style="max-width: 896px;min-width:320px; margin: 16px auto;">
							<div v-for="historyItem in chat_msg.history">
								<!---问题--->
								<div class="question_item" v-if="historyItem.role == 'user'">
									<div class="question_item_container">
										<!--问题头像-->
										<div class="question_item_avatar">
											<el-button @mouseover="questionEdit = true"
												@mouseleave="questionEdit = false">
												<template #icon>
													<svg-icon icon="icon-edit" v-if="questionEdit"  @click="editQuestion(historyItem.content)"></svg-icon>
													<svg-icon icon="icon-user" v-else></svg-icon>
												</template>
											</el-button>
										</div>
										<!--问题内容-->
										<div class="question_item_content">
											<div>{{ historyItem.content }}</div>
										</div>
									</div>
								</div>
								<!---回答--->
								<div class="ans_item"
									v-if="historyItem.role == 'assistant' || historyItem.role == 'system'">
									<div class="ans_item_avatar">
										<!--回答头像-->
										<div>
											<el-button>
												<template #icon>
													<svg-icon icon="icon-user"></svg-icon>
												</template>
											</el-button>
										</div>
									</div>
									<!--回答内容-->
									<div class="ans_item_content">
										<TextComponent ref="textRef" :text="historyItem.content" :loading="false"
											:asRawText="false" />
									</div>
								</div>
							</div>
							<div v-for="data in chat_msg.chatBotDatas">
								<!---问题--->
								<div class="question_item">
									<div class="question_item_container">
										<!--问题头像-->
										<div class="question_item_avatar">
											<el-button @mouseover="questionEdit = true"
												@mouseleave="questionEdit = false">
												<template #icon>
													<svg-icon icon="icon-edit" v-if="questionEdit"></svg-icon>
													<svg-icon icon="icon-user" v-else></svg-icon>
												</template>
											</el-button>
										</div>
										<!--问题内容-->
										<div class="question_item_content">
											<div>{{ data.userCt }}</div>
										</div>
									</div>
								</div>
								<!---回答--->
								<div class="ans_item">
									<div class="ans_item_avatar">
										<!--回答头像-->
										<div>
											<el-button>
												<template #icon>
													<svg-icon icon="icon-user"></svg-icon>
												</template>
											</el-button>
										</div>
									</div>
									<!--回答内容-->
									<div class="ans_item_content">
										<TextComponent ref="textRef" :text="data.assistantCt"
											:loading="data.isLoading" />
									</div>
								</div>
							</div>

						</div>
					</el-scrollbar>
				</div>

				<!--尾部-->
				<Footler ref="footlerRef" :ElNotificationErr="ElNotificationErr" :historyId="curHistoryId" :agentId="curAgent.agent_id"
					@update:cur-model="item => curModel = item" @update:chatBotDataUser="updateChatBotDatasUser" @update:chatBotDatAssert="updateChatBotDatas"
					@update:selectAgent="selectAgent" :sendContent="sendContent" />
			</el-main>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted, onUnmounted, watch, onUpdated, nextTick } from 'vue'
import { ElNotification, ElScrollbar, ElMessage,ElMessageBox } from 'element-plus'
import TextComponent from '@/components/Message/Text.vue'
import HistoryAside from '@/views/chat/historyAside.vue'
import Footler from '@/views/chat/footler.vue'
import { useGetHistoryDetailApi } from '@/api/chat'



const curHistoryId = ref('')
const historyRef = ref()

const ElNotificationErr = (err: any) => {
	ElNotification({
		title: err.message,
		message: err?.response?.data,
		type: 'error'
	})
}

// 关闭历史记录siber
const chatHistoryDisplay = ref(true)


const chat_msg = reactive({
	history: [],
	chatBotDatas: []
})


// 问题头像
const questionEdit = ref(false)

// 当前模型
const curModel = ref('')

// 当前智能体
const curAgent = reactive({
	agent_id: '',
	agent_title: '',
	token_count: 0
})

// 重新发送的问题
const sendContent = ref('')

const footlerRef = ref()

// 对话框滚动条滚动到底部
const scrollbarRef = ref<InstanceType<typeof ElScrollbar>>()
const scrollbarToBotom = async (smooth: boolean) => {
	await nextTick();
	const { scrollTop, clientHeight, scrollHeight } = scrollbarRef.value.wrapRef;
	const isAtBottom = scrollTop + clientHeight >= scrollHeight;
	if (isAtBottom) {
		return
	} else {
		if (smooth) {
			// 缓慢滚动
			let baseHeight = 20; // 每次滚动的距离
			const height = scrollTop + clientHeight
			const intervalId = setInterval(() => {
				baseHeight += 50;
				const newScrollTop = height + baseHeight;
				scrollbarRef?.value?.setScrollTop(newScrollTop);
				if (newScrollTop >= scrollHeight) {
					clearInterval(intervalId);
				}
			}, 200);
		} else {
			scrollbarRef?.value?.setScrollTop(scrollHeight);
		}
	}

}

watch([scrollbarRef, chat_msg], ([newScrollVal, newChatVal], [oldScrollVal, oldChatVal]) => {
	if (newScrollVal || newChatVal.length > 0) {
		scrollbarToBotom(newChatVal.length > 0 ? true : false)
	}
})

// 选择智能体
const selectAgent = (historyId: any) => {
	// 刷新历史记录
	curHistoryId.value = historyId
	historyRef.value.refreshAndSelectFirstHistory(true)
}                                                                                                                                                                           

// 选择的历史记录
const selectHistoryItem = (data:any) => {
	// 清空数据
	const historyId = data.historyId
	const isClearChat = data.isClearChat
	curHistoryId.value = historyId
	
	// 获取历史记录详情
	useGetHistoryDetailApi({ "id": historyId }).then(res => {
		// 填充数据
		curModel.value = res.model_name
		curAgent.agent_id = res.agent_id
		curAgent.agent_title = res.agent_title
		curAgent.token_count = res.all_token_counts
		if(isClearChat){
			//表明是直接点击的历史记录
			chat_msg.chatBotDatas = []
			chat_msg.history = res.content
			footlerRef.value.init()
		}else{
			//表明是发送的消息，不是点击的历史记录
			// 填充数据
			chat_msg.history = []
		}
		
	})
}

// 发送按钮事件,返回回答
const updateChatBotDatas = (data: any) => {
	// 使用深拷贝
	data = JSON.parse(JSON.stringify(data))
	chat_msg.chatBotDatas[chat_msg.chatBotDatas.length - 1] = data
	if (curHistoryId.value == '') {
		// 刷新历史列表,不清空chat
		historyRef.value.refreshAndSelectFirstHistory(false)
	}
}
// 首先发送
const updateChatBotDatasUser = (data: any) => {
	// 使用深拷贝
	data = JSON.parse(JSON.stringify(data))
	chat_msg.chatBotDatas.push(data)
}

// 初始化所有页面
const refreshHistory =(isAlert:boolean)=>{
	if(curHistoryId.value == ''){
		if(isAlert){
			ElMessage.success('已经是最新对话')
		}
	}
	// 历史记录
	historyRef.value.clearAll()
	// 对话部分
	init()
	// 尾部
	footlerRef.value.init()
}

const init=() => {
	// 初始化数据
	chat_msg.chatBotDatas = []
	chat_msg.history = []
	curHistoryId.value=''
	curAgent.agent_id=''
	curAgent.agent_title=''
	curAgent.token_count = 0
}

const editQuestion=(data:string) =>{
	// 重新发送内容
	ElMessageBox.prompt('请输入发送的内容', '发送', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		inputPattern: /.+?/,
		inputErrorMessage: '内容不能为空',
		inputValue: data
	})
	.then(({ value }) => {
		sendContent.value = value
	})
}

onMounted(() => {
	init()
})
</script>


<style lang="scss" scoped>
.chat_card_aside {
	padding: 24px 10px 8px 10px;
	border-right: 1px solid rgba(237, 239, 245, .45);
	min-height: calc(100vh - 19px);
	background-color: #fff;
}

.chat_card_main {
	background-color: rgb(246, 247, 251);
	min-height: calc(100vh - 19px);
	padding: 20px 0px;
	top: 0px;
	position: relative;
}

.chat_card {
	.el-card {
		border: none !important;
	}
}

.command_title {
	color: rgb(0, 0, 0, 0.88);
	font-size: 18px;
	font-weight: 600;
}

.command_close {
	display: flex;
	float: right;
	cursor: pointer;
}

.chat_card_aside_title {
	padding: 8px 8px 8px 0px;
}

:deep .el-tabs--card>.el-tabs__header .el-tabs__nav {
	border-style: none !important;
}

:deep .el-tabs__header {
	border-style: none !important;
}

:deep .el-tabs--card>.el-tabs__header .el-tabs__item {
	background: rgb(238, 237, 255);
	border-radius: 14px;
	color: #585a73;
	cursor: pointer;
	font-size: 12px;
	margin-right: 8px;
	text-align: center;
	white-space: nowrap;
}

:deep .el-tabs--card>.el-tabs__header .el-tabs__item.is-active {
	background-color: #615ced;
	color: #fff;
}

:deep .el-tabs__item {
	padding: 4px 8px !important;
	height: 27px;
}

:deep .el-dropdown-menu__item:hover {
	background-color: #615ced;
	color: #fff;
}

:deep .el-collapse-item__header {
	padding-left: 5px;
}

:deep .el-collapse-item__content {
	padding-left: 5px;
}

.chat_tilte_bg {
	font-size: 16px;
	font-weight: 600;
	color: #000;
}

.chat_listItem {
	background: rgb(238, 237, 255);
	border: 1px solid transparent;
	border-radius: 12px;
	cursor: pointer;
	font-family: PingFang SC;
	font-size: 13px;
	font-weight: 400;
	line-height: 20px;
	margin-bottom: 8px;
	padding: 8px 12px 12px;
	display: flex;
}

.chat_listItem:hover {
	background: rgb(238, 237, 255);
	border: 1px solid #615ced;
	box-sizing: border-box
}

.chat_listItem_title {
	color: #2c2c36;
	font-family: PingFang SC;
	font-size: 14px;
	font-weight: 500;
	letter-spacing: 0;
	line-height: 24px;
	margin: auto 0;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap
}

.chat_listItem_content {
	-webkit-box-orient: vertical;
	color: #585a73;
	overflow: hidden;
	text-overflow: ellipsis
}

:deep .el-slider__input {
	width: 90px;
}

.slider_margin_left_10 {
	margin-left: 10px;
	margin-bottom: 5px;
}

:deep .el-popper {
	max-width: 266px;
}

.model-option-container {
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 100%;
}

// .model-label {
// 	float: left;
// 	font-size: 14px;
// 	color: var(--el-text-color-primary);
// }

// .model-details-info {
// 	display: inline-block;
// 	font-size: 13px;
// 	color: var(--el-text-color-secondary);
// 	max-width: 100px;
// 	width: 100px;
// 	text-overflow: ellipsis;
// 	white-space: nowrap;
// 	overflow: hidden;
// }

.chat_history_expend {
	position: absolute;
	top: 0;
	left: 0px;
	height: 100%;
	width: 14px;
	background-color: rgba(0, 0, 0, 0);
	cursor: pointer;
	transition: all ease 0.3s;
	display: flex;
	align-items: center;
	z-index: 999;
}



:deep .el-textarea__inner {
	resize: none !important;
	padding: 0px;
}

.ans_item {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
}

.ans_item_avatar :deep .el-button {
	padding: 8px 8px;
}

.ans_item_content {
	background: #fff;
	border: 1px solid transparent;
	border-radius: 12px;
	display: flex;
	flex-direction: column;
	flex-grow: 1;
	flex-shrink: 1;
	overflow: hidden;
	position: relative;
	box-sizing: border-box;
	max-width: 100%;
	margin-top: 10px;
	margin-bottom: 10px;
	border-radius: 10px;
	padding: 10px;
	font-size: 14px;
	-webkit-user-select: text;
	-moz-user-select: text;
	user-select: text;
	word-break: break-word;
	transition: all ease 0.3s;
	width: 100%;
}

.question_item {
	display: flex;
	flex-direction: row-reverse;
}

.question_item>.question_item_container {
	align-items: flex-end;
}

.question_item_avatar {
	flex-direction: row-reverse;
}

.question_item_content {
	background: #e0dfff;
	border: 1px solid transparent;
	border-radius: 12px;
	display: flex;
	flex-direction: column;
	flex-grow: 1;
	flex-shrink: 1;
	overflow: hidden;
	position: relative;
	box-sizing: border-box;
	max-width: 100%;
	margin-top: 10px;
	border-radius: 10px;
	padding: 10px;
	font-size: 14px;
	-webkit-user-select: text;
	-moz-user-select: text;
	user-select: text;
	word-break: break-word;
	transition: all ease 0.3s;
}

// .markdown-body {
// 	box-sizing: border-box;
// 	min-width: 200px;
// 	max-width: 980px;
// 	margin: 0 auto;
// 	padding: 45px;
// }

// @media (max-width: 767px) {
// 	.markdown-body {
// 		padding: 15px;
// 	}
// }</style>
