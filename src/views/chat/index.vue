<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="300px" class="chat_card_aside" v-show="chatHistoryDisplay">
				<HistoryAside ref="historyRef" @click:history="item => selectHistoryItem(item)"
					@refresh:history="refreshHistory" />
			</el-aside>

			<el-main class="chat_card_main">
				<div class="chat_history_expend" @click="chatHistoryDisplay = !chatHistoryDisplay">
					<svg-icon icon="icon-arrow-expand" :size="'25'" v-show="!chatHistoryDisplay"></svg-icon>
					<svg-icon icon="icon-arrow-fold" :size="'25'" v-show="chatHistoryDisplay"></svg-icon>
				</div>
				<!--头部-->
				<div style="min-height: 40px;border-bottom: 1px solid #ebeef5;">
					<el-row style="padding: 0px 20px;" justify="space-between">
						<el-col :xs="14" :sm="16" :md="16" :lg="16" :xl="16">
							模型名称: <span style="color: #00BFFF;">{{ curModel }}</span>
						</el-col>
						<el-col :xs="10" :sm="8" :md="8" :lg="8" :xl="8" style="display: flex;justify-content: end;">
							<span style="color: #a6a6a6;">本次对话累计消耗了 {{ curAgent.token_count }} tokens</span>
						</el-col>
					</el-row>
					<el-row style="padding: 0px 20px;">
						<el-col :span="16">
							角色体: <span style="color: #00BFFF;">{{ curAgent.agent_title }}</span>
						</el-col>
					</el-row>
				</div>
				<!--内容-->
				<div class="chat_main_content">
					<el-scrollbar max-height="100%" style="width: 100%;" ref="scrollbarRef">
						<div style="max-width: 896px;min-width:320px; margin: 16px auto;">
							<div v-for="(historyItem, index) in chat_msg.history">
								<!---问题--->
								<div class="question_item" v-if="historyItem.role == 'user'">
									<div class="question_item_container">
										<!--问题头像-->
										<div class="question_item_avatar">
											<el-button>
												<template #icon>
													<svg-icon :size="'25'" :icon="curAgent.user_icon" />
												</template>
											</el-button>
										</div>
										<!--问题内容-->
										<div v-if="Array.isArray(historyItem.content)"
											v-for="(item, index) in historyItem.content" :key="index">
											<div class="question_item_file" v-if="item.type === 'image_url'">
												<div class="question_item_file_contain">
													<el-image style="width: 100px; height: 100px"
														:src="item.image_url.url" :zoom-rate="1.2" :max-scale="7"
														:min-scale="0.2" :preview-src-list="[item.image_url.url]"
														show-progress :initial-index="4" fit="cover" />
												</div>
											</div>
										</div>
										<div v-else class="question_item_content">
											<div class="preserve-format">{{ historyItem.content }}</div>
										</div>
									</div>
									<!--悬浮的div-->
									<div class="feature_tool">

										<div class="feature_tool_item" @click="snipHistory(index)">
											<el-tooltip effect="dark" content="在此消息后分支聊天" placement="top">
												<svg-icon :size="'20'" icon="icon-lianjie"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="copyMessage(historyItem.content)">
											<el-tooltip effect="dark" content="复制消息" placement="top">
												<svg-icon :size="'20'" icon="icon-chat_copy"></svg-icon>
											</el-tooltip>
										</div>
										<div v-if="!Array.isArray(historyItem.content)" class="feature_tool_item"
											@click="editMessage(historyItem.content, index)">
											<el-tooltip effect="dark" content="编辑消息" placement="top">
												<svg-icon :size="'20'" icon="icon-edit_save"></svg-icon>
											</el-tooltip>
										</div>
										<div v-if="!Array.isArray(historyItem.content)" class="feature_tool_item"
											@click="editQuestion(historyItem.content)">
											<el-tooltip effect="dark" content="重新编辑" placement="top">
												<svg-icon :size="'20'" icon="icon-edit"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="delCurMessage(index)">
											<el-tooltip effect="dark" content="删除消息" placement="top">
												<svg-icon :size="'20'" icon="icon-shanchu"></svg-icon>
											</el-tooltip>
										</div>
									</div>
								</div>
								<div class="question_item" v-if="historyItem?.type == 'file'">
									<div class="question_item_container">
										<!--问题头像-->
										<div class="question_item_avatar">
											<el-button>
												<template #icon>
													<svg-icon :size="'25'" :icon="curAgent.user_icon"></svg-icon>
												</template>
											</el-button>
										</div>
										<!--问题内容-->
										<div class="question_item_file">
											<!--展示文件内容--->
											<div class="question_item_file_contain">
												<div class="question_item_file_icon"><svg-icon :size="'40'"
														icon="icon-file"></svg-icon>
												</div>
												<div class="question_item_file_content">
													<div>{{ historyItem?.file }}</div>
												</div>
											</div>
										</div>
									</div>
									<!--悬浮的div-->
									<div class="feature_tool">
										<div class="feature_tool_item" @click="downChatFileFn(historyItem)">
											<el-tooltip effect="dark" content="下载" placement="top">
												<svg-icon :size="'20'" icon="icon-down_file"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="delCurMessage(index)">
											<el-tooltip effect="dark" content="删除" placement="top">
												<svg-icon :size="'20'" icon="icon-shanchu"></svg-icon>
											</el-tooltip>
										</div>
									</div>
								</div>
								<!---回答--->
								<div class="ans_item"
									v-if="historyItem.role == 'assistant' || (historyItem.role == 'system' && systemOutput)">
									<div class="ans_item_avatar">
										<!--回答头像-->
										<div>
											<el-button>
												<template #icon>
													<svg-icon :size="'25'" :icon="curAgent.assistant_icon"></svg-icon>
												</template>
											</el-button>
										</div>
									</div>
									<!--回答内容-->
									<div class="ans_item_content">
										<TextComponent ref="textRef" :text="historyItem.content" :loading="false"
											:asRawText="false" />
									</div>
									<!--悬浮的div-->
									<div class="feature_tool">
										<div class="feature_tool_item" @click="snipHistory(index)">
											<el-tooltip effect="dark" content="在此消息后分支聊天" placement="top">
												<svg-icon :size="'20'" icon="icon-lianjie"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="copyMessage(historyItem.content)">
											<el-tooltip effect="dark" content="复制消息" placement="top">
												<svg-icon :size="'20'" icon="icon-chat_copy"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="editMessage(historyItem.content, index)">
											<el-tooltip effect="dark" content="编辑消息" placement="top">
												<svg-icon :size="'20'" icon="icon-edit_save"></svg-icon>
											</el-tooltip>
										</div>
										<div class="feature_tool_item" @click="delCurMessage(index)">
											<el-tooltip effect="dark" content="删除消息" placement="top">
												<svg-icon :size="'20'" icon="icon-shanchu"></svg-icon>
											</el-tooltip>
										</div>
									</div>
								</div>
							</div>
							<div v-for="data in chat_msg.chatBotDatas">
								<div v-if="data.fileData">
									<div v-if="data?.fileData.showParse">
										<!---展示文件解析-->
										<div class="ans_item">
											<div class="ans_item_avatar">
												<!--回答头像-->
												<div>
													<el-button>
														<template #icon>
															<svg-icon :size="'25'"
																:icon="curAgent.assistant_icon"></svg-icon>
														</template>
													</el-button>
												</div>
											</div>
											<!--回答内容-->
											<div class="ans_item_content">
												<!----解析文件--->
												<div v-if="data?.fileData.parseLoading">
													<div> 文件解析中。。。。</div>
													<div class="file-loading-container">
														<div class="file-load-moving">
															<svg-icon className="file-load-icon"
																icon="icon-loading"></svg-icon>
														</div>
													</div>

												</div>
												<div
													v-if="!data?.fileData.parseLoading && !data?.fileData.parseErrMsg && data?.fileData.parseErrMsg != ''">
													<div>文档解析完成• ·̫ •</div>
												</div>
												<div v-if="!data?.fileData.parseLoading && data?.fileData.parseErrMsg">
													<div>{{ data?.fileData.parseErrMsg }}</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div v-else>
									<!---问题--->
									<div class="question_item" v-if="data?.type != 'file'">
										<div class="question_item_container">
											<!--问题头像-->
											<div class="question_item_avatar">
												<el-button>
													<svg-icon :size="'25'" :icon="curAgent.user_icon" />
												</el-button>
											</div>
											<!--问题内容-->
											<div class="question_item_content">
												<div class="preserve-format">{{ data.userCt }}</div>
											</div>
										</div>
										<!--悬浮的div-->
										<div class="feature_tool">
											<div class="feature_tool_item" @click="copyMessage(data.userCt)">
												<el-tooltip effect="dark" content="复制消息" placement="top">
													<svg-icon :size="'20'" icon="icon-chat_copy"></svg-icon>
												</el-tooltip>
											</div>
											<div class="feature_tool_item" @click="editQuestion(data.userCt)">
												<el-tooltip effect="dark" content="重新编辑" placement="top">
													<svg-icon :size="'20'" icon="icon-edit"></svg-icon>
												</el-tooltip>
											</div>
										</div>
									</div>
									<div class="question_item" v-if="data?.type == 'file'">
										<div class="question_item_container">
											<!--问题头像-->
											<div class="question_item_avatar">
												<el-button>
													<template #icon>
														<svg-icon :size="'25'" :icon="curAgent.user_icon"></svg-icon>
													</template>
												</el-button>
											</div>
											<!--问题内容-->
											<div class="question_item_file">
												<!--展示文件内容--->
												<div class="question_item_file_contain">
													<div class="question_item_file_icon"><svg-icon :size="'40'"
															icon="icon-file"></svg-icon></div>
													<div class="question_item_file_content">{{ data?.file }}</div>
												</div>
											</div>
										</div>
										<!--悬浮的div-->
										<div class="feature_tool">
											<div class="feature_tool_item" @click="downChatFileFn(data)">
												<el-tooltip effect="dark" content="下载" placement="top">
													<svg-icon :size="'20'" icon="icon-down_file"></svg-icon>
												</el-tooltip>
											</div>
										</div>
									</div>
									<!---回答--->
									<div class="ans_item" v-if="data?.type != 'file'">
										<div class="ans_item_avatar">
											<!--回答头像-->
											<div>
												<el-button>
													<template #icon>
														<svg-icon :size="'25'"
															:icon="curAgent.assistant_icon"></svg-icon>
													</template>
												</el-button>
											</div>
										</div>
										<!--回答内容-->
										<div class="ans_item_content">
											<TextComponent ref="textRef" :text="data.assistantCt"
												:loading="data.isLoading" />
										</div>
										<!--悬浮的div-->
										<div class="feature_tool">
											<div class="feature_tool_item" @click="copyMessage(data.assistantCt)">
												<el-tooltip effect="dark" content="复制消息" placement="top">
													<svg-icon :size="'20'" icon="icon-chat_copy"></svg-icon>
												</el-tooltip>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</el-scrollbar>
				</div>

				<!--尾部-->
				<Footler ref="footlerRef" :ElNotificationErr="ElNotificationErr" :historyId="curHistoryId"
					:agentId="curAgent.agent_id" @update:cur-model-key="curModelKeyFn"
					@update:chatBotDataUser="updateChatBotDatasUser" @update:chatBotDatAssert="updateChatBotDatas"
					@update:selectAgent="selectAgent" @update:clear-history-all="clearHistoryAll"
					@update:chat-file-data="updateChatFileData" @update:refreshHistory="refreshHistoryFor"
					:sendContent="sendContent" />
			</el-main>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, watch, nextTick } from 'vue'
import { ElNotification, ElScrollbar, ElMessage, ElMessageBox } from 'element-plus'
import TextComponent from '@/components/Message/Text.vue'
import HistoryAside from '@/views/chat/historyAside.vue'
import Footler from '@/views/chat/footler.vue'
import { useGetHistoryDetailApi, useHistoryTokensApi, useDownChatFileApi, useUpdateHistoryApi, useSnipHistoryBuildApi } from '@/api/chat'
import { useModelDetailApi } from '@/api/model'
import { copyToClip } from '@/utils/copy'
import { isMobile } from '@/utils/tool'

const curHistoryId = ref('')
const historyRef = ref()

// 隐藏system显示
const systemOutput = ref(false)

const ElNotificationErr = (err: any) => {
	ElNotification({
		title: err.message,
		message: err?.response?.data,
		type: 'error'
	})
}

// 关闭聊天记录siber,是移动端的话就默认不展开
const chatHistoryDisplay = ref(!isMobile())


const chat_msg = reactive({
	history: [],
	chatBotDatas: []
})

// 当前模型
const curModel = ref('')

// 当前角色体
const initCurAgent = {
	agent_id: '',
	agent_title: '',
	token_count: 0,
	user_icon: 'icon-user',
	assistant_icon: 'icon-user'
}
const curAgent = reactive({ ...initCurAgent })
// 重置
const resetCurAgent = () => {
	Object.assign(curAgent, initCurAgent)
}

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

// 选择角色体
const selectAgent = (historyId: any) => {
	// 刷新聊天记录
	curHistoryId.value = historyId
	historyRef.value?.refreshAndSelectFirstHistory(true)
}

// 选择的聊天记录
const selectHistoryItem = (data: any) => {
	// 是移动端的话，隐藏历史记录
	if (isMobile()) {
		chatHistoryDisplay.value = false
	}
	// 清空数据
	const historyId = data.historyId
	const isClearChat = data.isClearChat
	curHistoryId.value = historyId

	// 获取聊天记录详情
	useGetHistoryDetailApi({ "id": historyId }).then(res => {
		data = res.data
		const agentData = res.data?.agent_data
		// 填充数据
		curAgent.token_count = data.all_token_counts
		curAgent.agent_id = data.agent_id
		curModel.value = agentData.model_name
		curAgent.agent_title = agentData.title
		curAgent.user_icon = agentData.user_icon ? agentData.user_icon : 'icon-user'
		curAgent.assistant_icon = agentData.assistant_icon ? agentData.assistant_icon : 'icon-user'
		// 更新聊天记录数量
		historyRef.value.setHistoryCount(historyId, data.count)
		if (isClearChat) {
			//表明是直接点击的聊天记录
			chat_msg.chatBotDatas = []
			chat_msg.history = data.content
			// 把模型名称传过去
			footlerRef.value.init(agentData.model_key)
		} else {
			//表明是发送的消息，不是点击的聊天记录
			// 填充数据
			chat_msg.history = []
		}

	})
}

// 发送按钮事件,返回回答
const updateChatBotDatas = (data: any) => {
	// 使用深拷贝
	data = JSON.parse(JSON.stringify(data))
	const streamLoading = data.streamLoading
	chat_msg.chatBotDatas[chat_msg.chatBotDatas.length - 1] = data
	if (curHistoryId.value == '') {
		// 刷新历史列表,不清空chat
		historyRef.value?.refreshAndSelectFirstHistory(false)
	} else {
		if (!streamLoading) {
			// 等stram流加载完了再统计token和对话
			const historyId = curHistoryId.value
			// 刷新token和对话
			useHistoryTokensApi({ id: historyId }).then(res => {
				data = res.data
				const count = data.count
				curAgent.token_count = data.all_token_counts
				historyRef.value.setHistoryCount(historyId, count)
			})
		}

	}

}
// 首先发送
const updateChatBotDatasUser = (data: any) => {
	// 使用深拷贝
	data = JSON.parse(JSON.stringify(data))
	chat_msg.chatBotDatas.push(data)
}

// 更新发送文件
const updateChatFileData = (data: any) => {
	// 使用深拷贝
	data = JSON.parse(JSON.stringify(data))
	chat_msg.chatBotDatas[chat_msg.chatBotDatas.length - 1] = data
}

// 初始化所有页面
const refreshHistory = (isAlert: boolean) => {
	if (curHistoryId.value == '') {
		if (isAlert) {
			ElMessage.success('已经是最新对话')
		}
	}
	// 聊天记录
	historyRef.value.clearAll()
	// 对话部分
	init()
	// 尾部
	footlerRef.value.init()
}

const init = () => {
	// 初始化数据
	chat_msg.chatBotDatas = []
	chat_msg.history = []
	curHistoryId.value = ''
	resetCurAgent()
}

const editQuestion = (data: string) => {
	// 重新发送内容
	ElMessageBox.prompt('请输入发送的内容', '重新发送', {
		confirmButtonText: '发送',
		cancelButtonText: '取消',
		inputPattern: /.+?/,
		inputErrorMessage: '内容不能为空',
		inputValue: data,
		inputType: 'textarea',
	})
		.then(({ value }) => {
			sendContent.value = value
		})
}

// 清除所有对话记录
const clearHistoryAll = () => {
	refreshHistory(false)
}

// 刷新指定聊天记录
const refreshHistoryFor = (history_id: string) => {
	const data = {
		"historyId": history_id,
		"isClearChat": true

	}
	selectHistoryItem(data)
}

const curModelKeyFn = (modelKey: string) => {
	if (modelKey) {
		// 查询模型详情
		useModelDetailApi({ "model_key": modelKey }).then(res => {
			const datas = res.data
			if (datas && datas.length > 0) {
				curModel.value = datas[0]?.model_name
			}

		})
	}
}

const downChatFileFn = (file: any) => {
	const file_path = file.file_path
	const file_name = file.file
	if (!file_path) {
		return ElNotification({
			title: '温馨提示',
			message: '下载失败，文件路径不存在',
			type: 'error'
		})
	}
	const a = document.createElement('a')
	a.href = useDownChatFileApi(file_name, file_path)
	document.body.appendChild(a)
	a.click()
	ElNotification({
		title: '温馨提示',
		message: '下载成功',
		type: 'success'
	})

}

// 复制消息
const copyMessage = (data: string) => {
	copyToClip(data).then(() => {
		ElNotification({
			title: '成功',
			message: '复制成功',
			type: 'success'
		})
	})
}

// 编辑消息
const editMessage = (historyContent: string, index: number) => {
	const roleItem = chat_msg.history[index]
	const historyId = curHistoryId.value
	// 重新发送内容
	ElMessageBox.prompt('请输入修改的内容', '保存', {
		confirmButtonText: '保存',
		cancelButtonText: '取消',
		inputPattern: /.+?/,
		inputErrorMessage: '内容不能为空',
		inputValue: historyContent,
		inputType: 'textarea',
	})
		.then(({ value }) => {
			roleItem.content = value
			const params = {
				"history_id": historyId,
				"contents_str": JSON.stringify(chat_msg.history),
			}
			useUpdateHistoryApi(params).then(res => {
				ElNotification({
					title: '成功',
					message: '操作成功',
					type: 'success'
				})
				// 刷新token和对话
				useHistoryTokensApi({ id: historyId }).then(res => {
					const data = res.data
					const count = data.count
					curAgent.token_count = data.all_token_counts
					historyRef.value.setHistoryCount(historyId, count)
				})

			}).catch((error) => {
				ElNotification({
					title: '操作失败',
					message: error.message,
					type: 'error'
				})
				// 还原原始数据
				roleItem.content = historyContent
			})
		})

}

// 删除消息
const delCurMessage = (index: number) => {
	ElMessageBox.confirm(
		'是否确认删除该对话？',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			// 删除
			chat_msg.history.splice(index, 1)
			const historyId = curHistoryId.value
			const params = {
				"history_id": historyId,
				"contents_str": JSON.stringify(chat_msg.history),
			}
			useUpdateHistoryApi(params).then(res => {
				ElNotification({
					title: '成功',
					message: '操作成功',
					type: 'success'
				})
				// 刷新token和对话
				useHistoryTokensApi({ id: historyId }).then(res => {
					const data = res.data
					const count = data.count
					curAgent.token_count = data.all_token_counts
					historyRef.value.setHistoryCount(historyId, count)
				})

			}).catch((error) => {
				ElNotification({
					title: '操作失败',
					message: error.message,
					type: 'error'
				})
			})
		})



}

// 新分支聊天
const snipHistory = (index: number) => {
	// 截取从0到index的数组
	const slicedHistory = chat_msg.history.slice(0, index + 1);
	const historyId = curHistoryId.value
	const params = {
		"history_id": historyId,
		"contents_str": JSON.stringify(slicedHistory),
	}
	useSnipHistoryBuildApi(params).then(res => {
		ElNotification({
			title: '成功',
			message: '操作成功',
			type: 'success'
		})
		// 刷新左侧记录并点击第一个
		// 刷新聊天记录
	curHistoryId.value = res.data.id
	historyRef.value.refreshAndSelectFirstHistory(true)
	}).catch((error) => {
		ElNotification({
			title: '操作失败',
			message: error.message,
			type: 'error'
		})
	})
}

onMounted(() => {
	init()
})
</script>


<style lang="scss" scoped>
.chat_card_aside {
	padding: 24px 5px 8px 10px;
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

:deep(.el-tabs--card)>.el-tabs__header .el-tabs__nav {
	border-style: none !important;
}

:deep(.el-tabs__header) {
	border-style: none !important;
}

:deep(.el-tabs--card)>.el-tabs__header .el-tabs__item {
	background: rgb(238, 237, 255);
	border-radius: 14px;
	color: #585a73;
	cursor: pointer;
	font-size: 12px;
	margin-right: 8px;
	text-align: center;
	white-space: nowrap;
}

:deep(.el-tabs--card)>.el-tabs__header .el-tabs__item.is-active {
	background-color: #615ced;
	color: #fff;
}

:deep(.el-tabs__item) {
	padding: 4px 8px !important;
	height: 27px;
}

:deep(.el-dropdown-menu__item):hover {
	background-color: #615ced;
	color: #fff;
}

:deep(.el-collapse-item__header) {
	padding-left: 5px;
}

:deep(.el-collapse-item__content) {
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

:deep(.el-slider__input) {
	width: 90px;
}

.slider_margin_left_10 {
	margin-left: 10px;
	margin-bottom: 5px;
}

:deep(.el-popper) {
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



:deep(.el-textarea__inner) {
	resize: none !important;
	padding: 0px;
}

.ans_item {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	margin-top: 10px;

	position: relative;
}

.ans_item_avatar :deep(.el-button) {
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
	margin-top: 10px;
	position: relative;
}

.feature_tool {
	display: none;
	flex-direction: row;
	align-items: center;
	justify-content: center;
	position: absolute;
	height: 40px;
	padding: 10px;
	min-width: 100px;
	bottom: -20px;
	right: 10px;
	background-color: rgba(250, 251, 255, 0.9);
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 4px;

	.feature_tool_item {
		margin-right: 10px;
		cursor: pointer;
	}

	.feature_tool_item &:last-child {
		padding: 0;
	}
}

.question_item:hover,
.ans_item:hover {
	background-color: rgba(237, 239, 245, .45);
}

.question_item:hover .feature_tool,
.ans_item:hover .feature_tool {
	display: flex;
}

.question_item>.question_item_container {
	display: flex;
	justify-content: flex-end;
	flex-direction: column;
}

.question_item_avatar {
	display: flex;
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

.question_item_file {
	background: rgb(246, 247, 251);
	border: 1px solid #ddd;
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

.preserve-format {
	white-space: pre-wrap;
	/* 保留空格和换行符 */
}

.question_item_file_contain {
	width: 100px;
	min-height: 100px;
	display: flex;
	flex-direction: column;

	.question_item_file_icon {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.question_item_file_content {
		text-align: center
	}
}

:deep(.file-load-icon) {
	width: 100px !important;
	height: 60px !important;
}

.file-loading-container {
	position: relative;
	width: 100%;
	height: 40px;
}

.file-load-moving {
	position: absolute;
	width: 100px;
	/* 根据实际需求调整 */
	height: 60px;
	/* 根据实际需求调整 */
	animation: file-moveRight 5s linear infinite;
}

@keyframes file-moveRight {
	0% {
		transform: translateX(0);
	}

	100% {
		transform: translateX(50vw);
	}
}

.chat_main_content{
	height: calc(100vh - 270px);
}

// 匹配移动端
@media (max-width: 768px) {
	.chat_main_content {
		padding: 15px;
	}
}




</style>
