<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="260px" class="chat_card_aside" v-if="chatHistoryDisplay">
				<HistoryAside :searchTxt="searchTxt" :historys="historys" :selectedHistory="selectedHistory" />
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
	<TextComponent ref="textRef" :text="chat_msg.system" :loading="false" :asRawText="false" />
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
				<Footler :ElNotificationErr="ElNotificationErr" @update:cur-model="item => curModel = item"
					@update:chat-bot-datas="item => chatBotDatas = item" />
			</el-main>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted, onUnmounted, watch, onUpdated, nextTick } from 'vue'
import { ElNotification, ElScrollbar, ElMessage } from 'element-plus'
import TextComponent from '@/components/Message/Text.vue'
import HistoryAside from '@/views/chat/historyAside.vue'
import Footler from '@/views/chat/footler.vue'
import { useChatApi, useModelsApi } from '@/api/chat'
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

const ElNotificationErr = (err: any) => {
	ElNotification({
		title: err.message,
		message: err?.response?.data,
		type: 'error'
	})
}

// 关闭历史记录siber
const chatHistoryDisplay = ref(true)

// 点击的历史记录
const selectedHistory = ref('')

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

// 当前模型
const curModel = ref('')
// 正在进行的对话数据
const chatBotDatas = ref<[chatBot]>([])

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

watch([scrollbarRef, chatBotDatas.value], ([newScrollVal, newChatVal], [oldScrollVal, oldChatVal]) => {
	if (newScrollVal || newChatVal.length > 0) {
		scrollbarToBotom(newChatVal.length > 0 ? true : false)
	}
})

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
