<template>
	<div class="chat_main_plane">
		<div class="chat_main_plane_icon">
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
					<mode-select v-model="curModel" style="width: 120px" />
				</el-popover>
			</div>
			<!--知识库-->
			<div class="chat_main_plane_space">
				<el-popover placement="top" trigger="hover" :show-arrow="false">
					<template #reference>
						<el-button title="知识库" round>
							<template #icon>
								<svg-icon icon="icon-zhihu"></svg-icon>
							</template>
						</el-button>
					</template>
					<knowledge-select v-model="knowledge" style="width: 120px" />
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
								<svg-icon icon="icon-conv" :size="'18'"></svg-icon>
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
								<svg-icon icon="icon-search-online" :size="'15'"></svg-icon>
							</template>
						</el-button>
					</template>
					在线搜索：<el-switch v-model="searchOnline"
						style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" />
				</el-popover>
			</div>
		</div>
		<!--发送框-->
		<div class="chat_input_container">
			<el-scrollbar :max-height="168" style="width: 100%">
				<!---上传的图片显示--->
				<div class="chat_file_Wrap" v-show="uploadShow">
					<div v-show="uploadImageShow">
						<el-upload v-model:file-list="fileList" class="disUoloadSty" ref="uploadImgRef"
							:headers="uploadheaders" :action="uploadHttpUrl" list-type="picture-card"
							:on-preview="handlePictureCardPreview" accept=".png,.jpg,.jpeg"
							:before-upload="handleImageBeforeUpload"
							:on-success="handleUploadSuccess"
							:on-change="handleUploadChange"
							:on-error="handleUploadError"
							>
							<el-icon>
								<Plus />
							</el-icon>
						</el-upload>
						<el-dialog v-model="dialogVisible">
							<img w-full :src="dialogImageUrl" alt="Preview Image" />
						</el-dialog>
					</div>
					<div v-show="uploadFileShow">
						<el-upload ref="uploadFileRef" v-model:file-list="fileList" class="file-uploader"
							:headers="uploadheaders" :action="uploadHttpUrl"
							:before-upload="handleFileBeforeUpload"
							:on-success="handleUploadSuccess"
							>
							<el-icon class="file-uploader-icon">
								<Plus />
							</el-icon>
						</el-upload>
					</div>
				</div>
			</el-scrollbar>
			<div class="chat_input">
				<!-- 上传文档-->
				<div class="chat_upload">
					<el-popover placement="top" trigger="hover" :show-arrow="false">
						<template #reference>
							<svg-icon icon="icon-upload" :size="25"></svg-icon>
						</template>
						<div class="history-menu">
							<el-tooltip effect="light" content="支持PDF、World、Execl,最大10M" placement="right"
								:offset="-5">
								<div class="history-menu-item" @click="uploadFileClick">
									<span><svg-icon icon="icon-upload-flie" /></span>上传文档
								</div>
							</el-tooltip>
							<el-tooltip effect="light" content="上传1张不超过10M的PNG/JPG的图片" placement="right" :offset="-5">
								<div class="history-menu-item" style="color: #181818 !important; border-top: none"
									@click="uploadImageClick">
									<span><svg-icon icon="icon-upload-image" /></span>上传图片
								</div>
							</el-tooltip>
						</div>
					</el-popover>
				</div>
				<div class="chat_textarea">
					<!-- <el-scrollbar :max-height="100" style="width: 100%"> -->
					<div class="chat_textarea_wrap">
						<el-input v-model="chatBotMst" :autosize="{ minRows: 1 }" type="textarea"
							class="chat_textarea_input" placeholder="Enter 发送，Shift + Enter 换行，/ 触发命令"
							@keyup="sendKeyClick">
						</el-input>
					</div>
					<!-- </el-scrollbar> -->
				</div>
				<div class="chat_input_send">
					<el-button v-if="chatData?.isLoading" color="#ff0000" circle size="large" :disabled="true">
						<template #icon>
							<svg-icon icon="icon-stop" :size="25"></svg-icon>
						</template>
					</el-button>	
					<el-button v-else-if="chatData?.streamLoading" color="#ff0000" @click="abortRequest" circle size="large">
						<template #icon>
							<svg-icon icon="icon-stop" :size="25"></svg-icon>
						</template>
					</el-button>
					<el-button v-else color="#626aef" title="发送" @click="sendBotMsgClick" circle size="large">
						<template #icon>
							<svg-icon icon="icon-send_right" :size="20"></svg-icon>
						</template>
					</el-button>
				</div>
			</div>
		</div>


		<Agent ref="agentRef" @submit="useSelectAgentApi" />
		<FnDialog ref="fnDialogRef" :historyId="props.historyId" @clear_all_history="clearHistoryAll"
			@refresh_history="refreshHistory" />
	</div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, watch } from 'vue'
import { ElNotification } from 'element-plus/es'
import { useModelsApi, useParseChatFileApi } from '@/api/chat'
import { fetchEventSource } from '@microsoft/fetch-event-source'
import Agent from '@/views/chat/agent.vue'
import ModeSelect from '@/components/model-select/index.vue'
import FnDialog from '@/views/chat/fnDialog.vue'
import knowledgeSelect from '@/components/knowledge-select/index.vue'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { file } from '@babel/types'
import { fa } from 'element-plus/es/locale'

interface Props {
	// 错误弹框
	ElNotificationErr: Function
	historyId: string
	agentId: string
	// 重新发送的内容
	sendContent: string
}

//正在对话
interface chatBot {
	// 用户输入
	userCt: string
	// 机器人回复
	assistantCt: string
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
	isLoading: false,
	streamLoading: false
})
// 对话输入框的数据
const chatBotMst = ref('')
// 智能体显示弹窗
const agentVisible = ref(false)
const agentRef = ref()

// 连续对话开关显示
const convOff = ref(true)
// 知识库
const knowledge = ref()
// 在线搜索显示
const searchOnline = ref(false)
//显示功能快捷键
const showFnVisible = ref(false)
const fnDialogRef = ref()

const mounted = onMounted(() => {
	// 获取所有的模型
	getModelList()
})

// 定义事件，方便传值
const emit = defineEmits(['update:chatBotDataUser', 'update:chatBotDatAssert', 'update:curModelKey', 'update:selectAgent', 'update:clearHistoryAll', 'update:refreshHistory','update:chatFileData'])

// 监听 chatBotMst 的变化
watch(curModel, (newVal, oldVal) => {
	emit('update:curModelKey', newVal)
})

// 获取所有的模型
const getModelList = () => {
	useModelsApi().then(res => {
		res.data.filter(item => item.default == true)
			.forEach(model => {
				// 获取默认的模型
				curModel.value = model.model_key
				console.log('curModel.value', curModel.value)
			})
	})
}

const sendKeyClick = (event: any) => {
	if (event.shiftKey) {
		//shift+enter 不触发此事件
		return
	}
	if (event.keyCode == 13) {
		// enter
		sendBotMsgClick(event)
	}
	// /键
	if (event.keyCode == 191) {
		fnDialogRef.value.init()
	}
}

let abortController = null
// 发送按钮
const sendBotMsgClick = async(event: any) => {
	if(uploadFileStatus.value == true){
		ElNotification({
			title: '提示',
			message: '文件正在上传中,请稍后',
			type: 'warning'
		})
		return
	}
	// 隐藏上传框
	uploadShow.value = false
	uploadImageShow.value = false
	uploadFileShow.value = false
	if (event.shiftKey) {
		//shift+enter 不触发此事件
		return
	}
	// 获取输入框的内容并去除换行符
	const message = chatBotMst.value.trim()
	if (!message) {
		ElNotification({
			title: '提示',
			message: '请输入要咨询的问题',
			type: 'warning'
		})
		return
	}

	if(uploadFilePath.value && uploadFileName.value !=''){
		chatBotMst.value = ''
		const res = await parseChatFile()
		if(!res){
			return
		}
	}

	const curMsg = {
		userCt: message,
		assistantCt: '',
		isLoading: true
	}
	chatData.userCt = message
	chatData.isLoading = true
	chatData.streamLoading = true
	// 传输数据
	emit('update:chatBotDataUser', curMsg)


	// 对话
	const data = {
		input_text: message,
		model_key: curModel.value,
		history_id: props.historyId,
		agent_id: props.agentId,
		conv_off: convOff.value,
		online_search: searchOnline.value,
		know_id: knowledge.value,
		file_path: uploadFilePath.value,
		file_name: uploadFileName.value,
		parse_file_id: parseFileName.value
	}

	const fetchStream = async (dataForm: any) => {
		abortController = new AbortController()
		chatData.assistantCt = ''
		try {
			chatData.assistantCt = ''
			const url = import.meta.env.VITE_API_URL as any
			const user = import.meta.env.VITE_USER_AUTHORIZATION as any
			await fetchEventSource(url + '/chat', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', 'authorization': user },
				body: JSON.stringify(dataForm),
				signal: abortController.signal, // 绑定中断信号
				openWhenHidden:true, 
				onopen: async (response) => {
					chatData.isLoading = true
					chatData.streamLoading = true
					if (response.status !== 200) {
						// 主动读取错误流
						const errorData = await response.json();
						throw new Error(errorData.error || '请求失败');
					}
				},
				onmessage: (e) => {
					const datas = e.data.replace('[TEXT]', '').replace('[/TEXT]', '').replace(/<br>/g, '\n')// 转换换行符为HTML
					chatData.assistantCt += datas
					chatData.isLoading = false
					emit('update:chatBotDatAssert', chatData)

				},
				onclose: () => {
					chatData.isLoading = false,
						chatData.streamLoading = false
					emit('update:chatBotDatAssert', chatData)
				},
				onerror: (err) => {
					// 禁用重试
					throw err
				}
			})
		} catch (error) {
			console.error('请求失败:', error)
			if (error.name === 'AbortError') {
				console.log('请求已被中止')
				chatData.assistantCt = "请求已被中止"
			} else {
				chatData.assistantCt = "请求失败：" + error.message
			}
			chatData.isLoading = false
			chatData.streamLoading = false
			emit('update:chatBotDatAssert', chatData)
		} finally {
			abortController = null
		}

	}

	fetchStream(data)
	chatBotMst.value = ''
	resetUpload()
}

// 中断请求方法
const abortRequest = () => {
	if (abortController) {
		abortController.abort() // 触发中止
		chatData.assistantCt += "\n\n 请求已被中止"
		chatData.isLoading = false
		chatData.streamLoading = false
		abortController = null
		emit('update:chatBotDatAssert', chatData)
	}
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
const init = (modelKey: string) => {
	chatData.assistantCt = ''
	chatData.userCt = ''
	chatData.isLoading = false
	// 对话输入框的数据
	chatBotMst.value = ''
	// 智能体显示弹窗
	agentVisible.value = false
	curModel.value = modelKey
	if (!modelKey) {
		// 不存在则获取所有的模型
		getModelList()
	}
}

// 清除所有历史记录的事件
const clearHistoryAll = () => {
	emit('update:clearHistoryAll')
}

// 刷新当前聊天记录
const refreshHistory = () => {
	emit('update:refreshHistory', props.historyId)
}


const fileList = ref<UploadUserFile[]>([])

const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
	dialogImageUrl.value = uploadFile.url!
	dialogVisible.value = true
}

const handleImageBeforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
	const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/jpg'];
	// 优化后的校验逻辑
	if (!ALLOWED_TYPES.includes(rawFile.type)) {
		ElMessage.error('仅支持 JPG/JPEG/PNG 格式的图片');
		return false;
	} else if (rawFile.size / 1024 / 1024 > 10) {
		ElMessage.error('只允许最大上传10MB的图片')
		return false
	}else if(fileList.value.length ==1){
		ElMessage.error('只允许上传一个图片')
		return false
	}
	uploadFileStatus.value = true
	return true
}

const handleFileBeforeUpload: UploadProps['beforeUpload'] = (rawFile) => {
	// 优化后的校验逻辑
	if (rawFile.size / 1024 / 1024 > 10) {
		ElMessage.error('只允许最大上传10MB的文件')
		return false
	}else if(fileList.value.length ==1){
		ElMessage.error('只允许上传一个文件')
		return false
	}
	uploadFileStatus.value = true
	return true
}

const handleUploadSuccess:UploadProps['onSuccess'] = (
  response,
  uploadFile
) => {
  if(response?.code != 200){
	ElMessage.error('上传文件失败，原因：'+response.msg)
	// 清除文件
	fileList.value = []
	resetUpload()
  }else{
	uploadFilePath.value= response?.data.file_path
	uploadFileName.value= response?.data.file_name
	// 增加页面显示
	const msg = {
		type: 'file',
		file: uploadFileName.value,
		file_path: uploadFilePath.value
	}
	emit('update:chatBotDataUser', msg)
  }
  uploadFileStatus.value = false
}


const handleUploadError: UploadProps['onError'] = (error, uploadFile, uploadFiles) => {
	console.log('文件上传失败', error)
	uploadFileStatus.value = false
}

// 上传
const uploadShow = ref(false)
// 上传图片
const uploadImageShow = ref(false)
// 上传文件
const uploadFileShow = ref(false)
const uploadImgRef = ref()
const uploadFileRef = ref()
// 上传响应的文件地址
const uploadFilePath = ref('')
// 上传响应文件名称
const uploadFileName = ref('')
// 解析文件名称
const parseFileName = ref()
// 文件上传状态
const uploadFileStatus = ref(false)

// 重置文件状态
const resetUpload = () => {
	uploadShow.value = false
	uploadImageShow.value=false
	uploadFileShow.value = false
	uploadFilePath.value = ''
	uploadFileName.value = ''
	fileList.value = []
	parseFileName.value = undefined
	uploadFileStatus.value = false
}

const uploadImageClick = () => {
	uploadShow.value = true
	uploadImageShow.value = true
	uploadFileShow.value = false
	const uploadRoot = uploadImgRef.value?.$el
	uploadRoot.querySelector('input[type="file"]').click()
}

const uploadFileClick = () => {
	uploadShow.value = true
	uploadImageShow.value = false
	uploadFileShow.value = true
	const uploadRoot = uploadFileRef.value?.$el
	uploadRoot.querySelector('input[type="file"]').click()
}

const url = import.meta.env.VITE_API_URL as any
const user = import.meta.env.VITE_USER_AUTHORIZATION as any
const uploadHttpUrl = ref(url + "/chat/upload")
const uploadheaders = ref({
	'authorization': user
})

// 解析文件
const parseChatFile =async ()=>{	
	const fileMsg = reactive({
		fileData:{
			showParse:true,
			parseLoading:true,
			parseErrMsg:undefined
		}
	})
	chatData.isLoading = true
	emit('update:chatBotDataUser', fileMsg)
	const params={
		file_path:uploadFilePath.value,
		file_name:uploadFileName.value,
		model_key:curModel.value
	}
	try {
    const response = await useParseChatFileApi(params);
	const errorMsg = response.data.error_msg
	if(errorMsg){
		fileMsg.fileData.parseErrMsg = errorMsg
	}
	parseFileName.value = response?.data.file_name
	if(response?.data.multimodal){
		// 视觉模型关闭
		fileMsg.fileData.showParse = false
	}
    // 处理响应数据
	} catch (error) {
		// 捕获并处理异常
		console.error('请求失败:', error);
		fileMsg.fileData.parseErrMsg = error.message
	}
	fileMsg.fileData.parseLoading = false
	chatData.isLoading = false
	emit('update:chatFileData', fileMsg)
	if(fileMsg.fileData.parseErrMsg){
		return false
	}
	return true
}
watch(
	() => props.sendContent,
	(newVal, oldVal) => {
		if (newVal) {
			chatBotMst.value = newVal
			sendBotMsgClick({})
		}
	}
)

defineExpose({
	init
})
</script>
<style lang="scss">
.chat_main_plane {
	// height: 115px;
	border-top: 1px solid #ebeef5;
	// padding: 10px;
	padding-top: 10px;
	// max-width: 1150px;
	margin: 16px auto;


	box-sizing: content-box;
	margin-top: 18px;
	max-width: 1150px;
	min-width: 320px;
	position: relative;
	transition: all .2s;
	width: calc(100% - 48px) !important;
	z-index: 999;
}


.chat_main_plane_icon {
	display: flex;
	flex-wrap: wrap;
	flex-direction: row;
}

.chat_input_container {
	align-items: center;
	background: #fff;
	border: 1.2px solid #ebeef5;
	border-radius: 20px;
	box-shadow: 0 12px 24px -16px rgba(54, 54, 73, .04), 0 12px 40px 0 rgba(51, 51, 71, .08), 0 0 1px 0 rgba(44, 44, 54, .02);
	display: flex;
	flex-direction: column;
	position: relative;
	transition: border .4s ease;
	width: 100%;

	margin-top: 10px !important;
	overflow: hidden;

	.chat_file_Wrap {
		align-items: flex-start;
		display: flex;
		flex-direction: column;
		flex-shrink: 0;
		margin-bottom: 20px;
		// max-height: 168px;
		// overflow-y: auto;
		padding: 20px 20px 0;
		width: 100%;
		overflow-y: hidden;
	}
}

.chat_input_container:has(.el-textarea__inner:focus) {
	border: 1px solid #626aef;
}

.chat_input {
	// margin-top: 10px !important;
	cursor: text;
	align-items: flex-end;
	display: flex;
	flex: 1;
	margin: 0 auto;
	overflow: auto;
	position: relative;
	width: 100%;
	z-index: 2;
	background-color: white;
	padding: 8px 8px 8px 16px
}

.chat_textarea {
	height: 100%;
	position: relative;
	width: calc(100% - 50px);
	flex: 1;

	.chat_textarea_wrap {
		height: 100%;
		margin-bottom: 10px;
		overflow: auto;
	}

	.chat_textarea_input>textarea {
		background: transparent !important;
		border: 0;
		box-shadow: none !important;
		caret-color: #26244c !important;
		color: #26244c !important;
		font-size: 16px;
		line-height: normal;
		line-height: 24px;
		margin-top: 8px;
		outline: 0;
		padding: 0 8px 0 0;
		resize: none;
		transition: none !important;
		width: 100%;
		overflow-y: hidden;
		height: 24px;
		min-height: 24px;
		max-height: 96px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
	}
}



.chat_input_send {
	align-items: center;
	border-radius: 20px;
	color: #fff;
	cursor: pointer;
	display: flex;
	flex-shrink: 0;
	height: 40px;
	justify-content: center;
	margin-left: 16px;
	position: relative;
}

.chat_upload {
	align-items: center;
	background: #fff;
	cursor: pointer;
	display: flex;
	height: 40px;
	justify-content: center;
	margin-right: 16px;
}

div {
	box-sizing: border-box
}

.disUoloadSty .el-upload-list__item {
	width: 60px !important;
	height: 60px !important;
}

.disUoloadSty .el-upload {
	width: 60px !important;
	height: 60px !important;
}

.file-uploader .el-upload {
	border: 1px dashed var(--el-border-color);
	border-radius: 6px;
	cursor: pointer;
	position: relative;
	overflow: hidden;
	transition: var(--el-transition-duration-fast);
}

.file-uploader .el-upload:hover {
	border-color: var(--el-color-primary);
}

.el-icon.file-uploader-icon {
	font-size: 28px;
	color: #8c939d;
	width: 60px;
	height: 60px;
	text-align: center;
}
</style>
