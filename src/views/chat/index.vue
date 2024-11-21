<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="260px" class="chat_card_aside" v-if="chatHistoryDisplay">
				<el-row>
					<el-input v-model="searchTxt" placeholder="搜索历史记录" style="border-radius: 20px;">
						<template #prefix>
							<svg-icon icon="icon-search"></svg-icon>
						</template>
					</el-input>
				</el-row>
				<div style="overflow: hidden;margin-top:20px">
					<el-scrollbar :max-height="computedHistoryMaxHeight">
						<ul>
							<li class="history_listItem"
								:class="{ 'history_listItem_active': selectedHistory === item.id }"
								v-for="item in historys" :key="item.id" @click="selectHistoryItem(item.id)">
								<span class="history_listItem_content">{{ item.content }}</span>
								<el-popover :visible="item.show == true" placement="right-start" :show-arrow="false"
									style="padding: 0px;">
									<div class="history-menu">
										<div class="history-menu-item">

											<span><svg-icon icon="icon-edit" /></span>重命名
										</div>
										<div class="history-menu-item">
											<span><svg-icon icon="icon-totop" /></span>置顶此对话
										</div>
										<div class="history-menu-item">
											<span><svg-icon icon="icon-delete" /></span>删除此对话
										</div>
									</div>
									<template #reference>
										<svg-icon class="history_listItem_icon" icon="icon-ellipsis"
											@click.stop="openHistoryMenu(item)"></svg-icon>
									</template>
								</el-popover>
							</li>
						</ul>
					</el-scrollbar>
				</div>
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
						 模型名称: <span style="color: #00BFFF;">{{curModel}}</span>	
						</el-col>
					</el-row>
					<el-row style="padding: 0px 20px;">
						<el-col :span="16">
						 智能体	
						</el-col>
					</el-row>
				</div>
				<!--内容-->
				<div style="height: calc(100vh - 270px - var(--theme-header-height));">
					<el-scrollbar max-height="100%" style="width: 100%;" ref="scrollbarRef">
						<div style="max-width: 1150px;margin: 16px auto;">
							<!--
							<div class="ans_item">
								<div class="ans_item_avatar">
									回答头像
									<div>
										<el-button>
											<template #icon>
												<svg-icon icon="icon-user"></svg-icon>
											</template>
										</el-button>
									</div>
								</div>
								回答内容
								<div class="ans_item_content">
									<TextComponent ref="textRef" :text="chat_msg.system" :loading="false"
										:asRawText="false" />
								</div>
							</div>
						-->
							<div v-for="historyItem in chat_msg.history">
								<!---问题--->
								<div class="question_item" v-if="historyItem.role == 'user'">
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
											<div>{{ historyItem.content }}</div>
										</div>
									</div>
								</div>
								<!---回答--->
								<div class="ans_item" v-if="historyItem.role == 'assistant'">
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
							<div v-for="data in chatBotDatas">
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
				<div class="chat_main_plane">
					<div class="chat_main_plane_icon">
						<!--上传-->
						<div class="chat_main_plane_space">
							<el-popover placement="top" trigger="hover" :show-arrow="false">
								<template #reference>
									<el-button title="上传"  round>
										<template #icon>
											<svg-icon icon="icon-upload"></svg-icon>
										</template>
									</el-button>
								</template>
								<div class="history-menu">
									<el-tooltip effect="light" content="支持PDF、World、Execl,最大100M" placement="right"
										:offset="-5">
										<div class="history-menu-item">
											<span><svg-icon icon="icon-upload-flie" /></span>上传文档
										</div>
									</el-tooltip>
									<el-tooltip effect="light" content="上传1张不超过10M的PNG/JPG的图片" placement="right"
										:offset="-5">
										<div class="history-menu-item"
											style="color: #181818 !important; border-top: none ;">
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
									<el-button title="大模型"  round>
										<template #icon>
											<svg-icon icon="icon-Checkpoint"></svg-icon>
										</template>
									</el-button>
								</template>
								<el-select :teleported="false" v-model="curModel" placeholder="请选择模型" style="width: 120px;">
									<el-option v-for="item in modelList" :key="item.label" :label="item.label"
										:value="item.label">
									</el-option>
								</el-select>
							</el-popover>

						</div>
					</div>

					<div class="chat_main_plane_label">
						<el-scrollbar :max-height="100" style="width: 100%;">
							<div class="chat_textarea">
								<el-input v-model="chatBotMst" :autosize="{ minRows: 2, maxRows: 6 }" type="textarea"
									input-style="height: 100%;width: 100%;border-radius: 10px;border: none;box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.00);background-color: white;color: black;font-family: inherit;padding: 10px 30px 10px 14px;resize: none;outline: none;box-sizing: border-box;resize:none !important;overflow: hidden;"
									placeholder="Enter 发送，Shift + Enter 换行，/ 触发补全，: 触发命令"
									@keyup.enter="sendBotMsgClick">
								</el-input>
							</div>
						</el-scrollbar>
						<div class="chat_input_send">
							<el-button color="#ff0000" disabled
								v-if="chatBotDatas?.[chatBotDatas.length - 1]?.isLoading">加载中</el-button>
							<el-button color="#626aef" @click="sendBotMsgClick" v-else>
								<div style="margin-right: 5px;">
									<svg-icon icon="icon-send_right" />
								</div>
								发送
							</el-button>

						</div>

					</div>

				</div>
			</el-main>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted, onUnmounted, watch, onUpdated, nextTick } from 'vue'
import { ElNotification, ElScrollbar, ElMessage } from 'element-plus'
import TextComponent from '@/components/Message/Text.vue'
import { useChatApi,useModelsApi } from '@/api/chat'
// 其他syspromt
const syspromts = ref([
	{
		title: '面试技巧',
		content: '作为一名资深HR，请结合面试岗位，用通俗易懂的言语提供实用可行的面试指南，面试岗位：会计'
	},
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}
	,
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}
	,
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}
	,
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}
	,
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}
	,
	{
		title: '账号涨粉助手',
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆'
	}

])
// 搜索
const searchTxt = ref('')
// 历史记录
const historys = ref([
	{
		id: 1,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 2,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 3,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 4,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 5,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 6,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},
	{
		id: 7,
		content: '输入您的行业类别，我会给您一些快速涨粉的建议。我的行业是：美妆',
		show: false
	},

])
// 保存点击的记录
const selectedHistory = ref('')
// 模型
const modes = ref([
	{
		label: 'lamam3',
		detailsInfo: 'lamam3描述,你是由哪个大模型训练的2'
	},
	{
		label: 'lamam3.1',
		detailsInfo: 'lamam3.1描述,你是由哪个大模型训练的2'
	},
	{
		label: 'lamam3.2',
		detailsInfo: 'lamam3.2描述'
	},
	{
		label: 'lamam3.3',
		detailsInfo: 'lamam3.3描述'
	},

])
// 选中模型
//const selectMode = ref({})

//const visible = ref(false)


// 点击历史记录 
const selectHistoryItem = (item: string) => {
	selectedHistory.value = item
}

// 右边其他参数
const themeHeaderHeight = ref(window.getComputedStyle(document.documentElement).getPropertyValue('--theme-header-height'));

// 计算最大高度
const computedMaxHeight = computed(() => {
	const headerHeight = parseFloat(themeHeaderHeight.value);
	return `calc(100vh - 19px - 130px - ${headerHeight}px)`;
});

// 左边历史记录
// 计算最大高度
const computedHistoryMaxHeight = computed(() => {
	const headerHeight = parseFloat(themeHeaderHeight.value);
	return `calc(100vh - 19px - 90px - ${headerHeight}px)`;
});


// 打开历史记录的菜单
const openHistoryMenu = (item: any) => {
	// 其他菜单隐藏
	closeHistoryMenu()
	item.show = true;
}

// 关闭菜单
const closeHistoryMenu = () => {
	historys.value.filter(item => item.show == true).find(item => item.show = false)
}


const ElNotificationErr = (err: any) => {
	ElNotification({
		title: err.message,
		message: err?.response?.data,
		type: 'error'
	})
}
const mounted = onMounted(() => {
	// 点击空白关闭历史记录菜单
	document.addEventListener('click', handleClickOutside);
	// 获取所有的模型
	getModelList();
});

const closeHistoryUnmounted = onUnmounted(() => {
	document.removeEventListener('click', handleClickOutside);
});

const handleClickOutside = (event: any) => {
	modes.value.forEach(item => {
		if (!event.target.closest('.el-popover')) {
			closeHistoryMenu()
		}
	});
};

// 关闭历史记录siber
const chatHistoryDisplay = ref(true)


// 对话
// 定义 HistoryItem 接口
interface HistoryItem {
	role: string;
	content: string;
}

interface historyChat {
	system: string,
	history: HistoryItem[],
	model_name: string,
	// single_turn: boolean,
	// temperature: number,
	// top_p: number,
	// n_choices: number,
	// stop_sequence: [],
	// token_upper_limit: number,
	// max_generation_token: number,
	// presence_penalty:number,
	// frequency_penalty: number,
	// logit_bias: number,
	// user_identifier: string,
	// stream: true,
	// metadata: {}
}

const chat_msg = ref<historyChat>()

chat_msg.value = {
	system: 'You are a helpful assistant.',
	history: [
		{
			role: 'user',
			content: 'python怎么使用vue前端项目'
		},
		{
			role: "assistant",
			content: "Python 可以与 Vue 前端项目集成的常见方式包括：\n\n1. 后端 API：使用 Flask 或 Django 等 Python 框架来创建 RESTful API，以提供数据给 Vue 应用程序。\n2. 服务端渲染 (SSR)：使用 Node.js 和 Express.js 作为服务端渲染层，使用 Python 作为数据处理层。\n3. Web 服务：使用 Python 的 Web 框架例如 Tornado 或 Pyramid 来提供一个 Web 服务，从而为 Vue 应用程序提供数据。\n\n下面是一个使用 Flask 和 Vue.js 的简单示例\n\n### Flask 后端 API\n\n创建一个名为 `app.py` 的文件，内容如下：\n```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n# 模拟数据\ndata = [\n    {\"id\": 1, \"name\": \"John\"},\n    {\"id\": 2, \"name\": \"Jane\"},\n]\n\n@app.route(\"/api/data\")\ndef get_data():\n    return jsonify(data)\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```\n运行该应用程序，打开浏览器，访问 `http://localhost:5000/api/data`，即可看到返回的 JSON 数据。\n\n### Vue.js 前端\n\n创建一个新的 Vue.js 项目，使用以下命令：\n```bash\nnpm install -g @vue/cli\nvue create vue-app\n```\n在 `src` 目录下创建一个名为 `api.js` 的文件，内容如下：\n```javascript\nimport axios from 'axios';\n\nconst api = axios.create({\n  baseURL: 'http://localhost:5000/api',\n});\n\nexport default api;\n```\n"
		}

	],
	model_name: 'llama-3.2-90b-vision-preview'
}

// 问题头像
const questionEdit = ref(false)

//正在对话
interface chatBot {
	// 用户输入
	userCt: string,
	// 机器人回复
	assistantCt: string,
	// 是否正在回复
	isLoading: boolean
}
// 正在进行的对话数据
const chatBotDatas = ref<[chatBot]>([])

// 对话输入框的数据
const chatBotMst = ref('')

// 发送按钮
const sendBotMsgClick = () => {
	let msg = chatBotMst.value
	if (!msg) {
		ElNotification({
			title: '提示',
			message: '请输入要咨询的问题',
			type: 'warning'
		})
	}
	const curMsg = {
		userCt: msg,
		assistantCt: '',
		isLoading: true
	}
	chatBotDatas.value.push(curMsg)
	// 对话
	useChatApi({ input_text: msg,model_name:curModel.value }).then(res => {
		chatBotDatas.value[chatBotDatas.value.length - 1].assistantCt = res
		chatBotDatas.value[chatBotDatas.value.length - 1].isLoading = false
	}).catch(err => {
		ElNotificationErr(err)
		chatBotDatas.value[chatBotDatas.value.length - 1].isLoading = false
	})
	// 清空发送的消息
	chatBotMst.value = ''
}

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
			}, 1000);
		} else {
			scrollbarRef?.value?.setScrollTop(scrollHeight);
		}
	}

}


watch([scrollbarRef, chatBotDatas.value], ([newScrollVal, newChatVal], [oldScrollVal, oldChatVal]) => {
	if (newScrollVal || newChatVal.length > 0) {
		scrollbarToBotom(newChatVal.length > 0 ? true : false)
	}
})

// 模型列表
const modelList = ref([])
// 当前模型
const curModel = ref()

// 获取所有的模型
const getModelList = () => {
	useModelsApi().then(res => {
		modelList.value = res
		modelList.value.filter(item => item.default == true).forEach(item => {
			curModel.value = item.label
		})
	}).catch(err => {
		ElNotificationErr(err)
	})
}


</script>


<style lang="scss" scoped>
.chat_card_aside {
	padding: 24px 10px 8px 10px;
	border-right: 1px solid rgba(237, 239, 245, .45);
	min-height: calc(100vh - 19px - var(--theme-header-height));
	background-color: #fff;
}

.chat_card_main {
	background-color: rgb(246, 247, 251);
	min-height: calc(100vh - 19px - var(--theme-header-height));
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

.history_listItem {
	align-items: center;
	border-radius: 12px;
	box-sizing: border-box;
	color: #26244c;
	cursor: pointer;
	display: flex;
	flex-shrink: 0;
	font-size: 14px;
	height: 36px;
	justify-content: space-between;
	margin-bottom: 12px;
	padding: 6px 16px;
	position: relative;
}

.history_listItem:hover {
	background: #f3f2ff;
	color: #615ced;
}

.history_listItem_active {
	background: #f3f2ff;
	color: #615ced;
}

.history_listItem_content {
	display: inline-block;
	max-width: 180px;
	overflow: hidden;
	position: relative;
	text-overflow: clip;
	white-space: nowrap
}

.history_listItem_icon {
	display: inline-block;
	height: 22px;
	line-height: 26px;
	margin-left: 2px
}

.model-option-container {
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 100%;
}

.model-label {
	float: left;
	font-size: 14px;
	color: var(--el-text-color-primary);
}

.model-details-info {
	display: inline-block;
	font-size: 13px;
	color: var(--el-text-color-secondary);
	max-width: 100px;
	width: 100px;
	text-overflow: ellipsis;
	white-space: nowrap;
	overflow: hidden;
}

.history-menu {
	align-items: center;
	background: #fff;
	box-sizing: border-box;
	display: flex;
	flex-direction: column;
	justify-content: center;
	overflow: hidden;
	padding: 4px 0;

	.history-menu-item {
		align-items: center;
		border-radius: 4px;
		color: #181818;
		cursor: pointer;
		display: flex;
		flex-direction: row;
		font-size: 14px;
		// height: 36px;
		margin-bottom: 2px;
		padding: 4px 12px;
		width: 140px
	}

	.history-menu-item>span {
		font-size: 20px;
		margin-right: 8px;
		margin-left: 8px;
	}
}

.history-menu-item:hover {
	background: #f7f8fc
}

.history-menu>div:last-of-type {
	border-top: 1px solid #e8eaf2;
	color: #e63224;
}

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

.markdown-body {
	box-sizing: border-box;
	min-width: 200px;
	max-width: 980px;
	margin: 0 auto;
	padding: 45px;
}

@media (max-width: 767px) {
	.markdown-body {
		padding: 15px;
	}
}
</style>
