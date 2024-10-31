<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="260px" class="chat_card_aside">
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
								<el-popover :visible="item.show == true" placement="right-start" :show-arrow="false" style="padding: 0px;">
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
				<div style="height: 40px;border-bottom: 1px solid #ebeef5;">
					<el-row style="padding: 0px 20px;">
						<el-col :span="16">
							<el-select v-model="selectMode" placeholder="Select" size="lager" style="width: 240px">
								<el-option v-for="item in modes" :key="item.value" :label="item.label"
									:value="item.detailsInfo">


									<div class="model-option-container">
										<span class="model-label">{{ item.label }}</span>
										<span class="model-details-info" :title="item.detailsInfo">
											<el-tooltip placement="right">
												<template #content>
													{{ item.detailsInfo }}
												</template>
												<span>{{ item.detailsInfo }}</span>
											</el-tooltip>
										</span>
									</div>


								</el-option>
							</el-select>
						</el-col>
						<el-col :span="8">
						</el-col>
					</el-row>
				</div>
			</el-main>
			<el-aside width="300px" class="chat_card_aside" v-if="commandCenterFlag">
				<el-row class="chat_card_aside_title">
					<el-col :span="16" class="command_title">指令中心</el-col>
					<el-col :span="8">
						<div class="command_close" title="关闭" @click="closeCommandCenter">
							<svg-icon icon="icon-close"></svg-icon>
						</div>
					</el-col>
				</el-row>
				<el-row>
					<el-col :span="20">
						<el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick" class="custom-tabs">
							<!-- 可见Tabs -->
							<el-tab-pane v-for="tab in visibleTabs" :key="tab.name" :label="tab.label"
								:name="tab.name" />
						</el-tabs>
					</el-col>
					<el-col :span="4">
						<!-- 下拉菜单 -->
						<el-dropdown @command="handleDropdownCommand">
							<div style="cursor: pointer;"> <svg-icon icon="icon-menu"></svg-icon></div>
							<template #dropdown>
								<el-dropdown-menu>
									<el-dropdown-item v-for="(tab, index) in tabs" :key="tab.name" :command="index">{{
										tab.label
									}}</el-dropdown-item>
								</el-dropdown-menu>
							</template>
						</el-dropdown>
					</el-col>
				</el-row>
				<el-row style="width: 100%;">
					<!-- 显示主题内容 -->
					<!--对话--->
					<el-col :span="24" v-show="activeTab == '1'">
						<el-collapse v-model="chat_model">
							<el-collapse-item title="模型API-KEY" name="1">
								<div>
									<el-input type="password" placeholder="模型API-KEY" show-password />
								</div>
							</el-collapse-item>
							<el-collapse-item title="Prompt" name="2">
								<div class="chat_tilte_bg">
									System prompt
								</div>
								<el-input clearable type="textarea" :rows="5" placeholder="System prompt" />
							</el-collapse-item>
							<el-collapse-item title="知识库" name="3">
								<div>
									<el-upload class="upload-demo" drag
										action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" multiple>
										<svg-icon icon="icon-cloud-upload"
											style="font-size: 50px;"><upload-filled /></svg-icon>
										<div class="el-upload__text">
											Drop file here or click to upload
										</div>
										<template #tip>
											<div class="el-upload__tip">
												jpg/png files with a size less than 500kb
											</div>
										</template>
									</el-upload>
								</div>
								<div>
									<el-button type="primary" style="background: #615ced;width: 100%;">总结</el-button>
								</div>
							</el-collapse-item>
						</el-collapse>
					</el-col>
					<!--参数--->
					<el-col :span="24" v-show="activeTab == '2'">
						<!--temperature-->
						<el-row>
							<el-col :span="12" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template #content> 用于控制输出概率分布“平滑度”的参数。<br />
										它影响着模型生成文本的随机性和多样性。<br />
										当温度值较高（例如1.0以上）：生成的文本更加随机和多样化。<br />
										当温度值较低（例如0.5以下）：生成的文本更加确定和集中。
									</template>
									<span>temperaturer</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.temperature" input-size="small" show-input :step="0.1" :min="0"
								:max="2" />
						</el-row>
						<!--top-p-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template #content> 核采样（Nucleus Sampling）。<br />
										它与 temperature 参数类似，都是用来调节生成文本的随机性和创造性。<br />
										p
										较小（例如0.1）：选择的词汇子集较小，生成的文本更加确定和集中，因为模型只会从概率最高的少数词汇中选择。这可能导致生成的文本更加保守和连贯，但缺乏多样性。<br />
										p
										较大（例如0.9）：选择的词汇子集较大，生成的文本更加随机和多样化，因为模型可以从更多的词汇中选择。这可能导致生成的文本更加创造性和有趣，但也可能降低连贯性。
									</template>
									<span>top-p</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.top_p" input-size="small" show-input :step="0.1" size="small"
								:min="0" :max="1" />
						</el-row>
						<!--n choices-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template #content> 从多个候选选项中选择 n 个选项的过程
									</template>
									<span>n choices</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.n_choices" input-size="small" show-input :step="1" size="small"
								:min="1" :max="10" />
						</el-row>
						<!--max_context-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template #content>模型在处理输入序列时所能考虑的最大上下文长度。<br />
										如果上下文窗口太短，生成的文本可能会缺乏连贯性；如果太长，计算成本会增加。
									</template>
									<span>max context</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.max_context" input-size="small" show-input :step="1"
								size="small" :min="1024" :max="100000" />
						</el-row>
						<!--max generations-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template
										#content>指模型在生成文本时的最大步数或最大长度。<br />具体来说，它定义了模型在生成过程中最多可以生成多少个词或字符。<br />一旦达到这个限制，生成过程就会停止。
									</template>
									<span>max generations</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.max_generations" input-size="small" show-input :step="1"
								size="small" :min="1024" :max="100000" />
						</el-row>
						<!--presence penalty-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template
										#content>是一种用于调整模型生成文本时已出现词汇的惩罚机制。<br />通过对已出现过的词汇施加惩罚，可以减少这些词汇再次出现的概率，从而提高生成文本的多样性和连贯性。<br />这种惩罚是基于词汇是否已经出现过，而不是出现的频率。<br />主要用于减少已出现词汇的再次出现，从而使生成的文本更加多样化和连贯。

									</template>
									<span>presence penalty</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.presence_penalty" input-size="small" show-input :step="0.01"
								size="small" :min="-2" :max="2" />
						</el-row>
						<!--frequency penalty-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template
										#content>一种用于调整模型生成文本时重复词汇出现频率的技术。<br />通过对频繁出现的词汇施加惩罚，可以减少这些词汇在生成文本中的重复出现，从而使生成的文本更加多样化和自然。
										<br />针对词汇在生成过程中出现的频率进行惩罚。具体来说，模型会根据每个词汇在生成过程中已经出现的次数来调整其概率。
									</template>
									<span>frequency penalty</span>
								</el-tooltip></el-col>
						</el-row>
						<el-row class="slider_margin_left_10">
							<!--滑块-->
							<el-slider v-model="parmars.frequency_penalty" input-size="small" show-input :step="0.01"
								size="small" :min="-2" :max="2" />
						</el-row>
						<!--logit bias-->
						<el-row>
							<el-col :span="24" class="chat_tilte_bg">
								<el-tooltip placement="left">
									<template #content>一个用于调整模型生成文本时特定词汇的概率的技术。<br />通过对某些词汇的 logit
										值进行偏置，可以影响模型生成这些词汇的可能性。<br />这对于控制生成文本的内容、风格或避免某些不希望出现的词汇非常有用。
									</template>
									<span>logit bias</span>
								</el-tooltip></el-col>
							<el-col :span="24" style="margin-top: 5px;"><el-input :rows="2" type="textarea"
									v-model="parmars.logit_bias" placeholder="word:likelihood" /></el-col>
						</el-row>
					</el-col>
					<!--其他--->
					<el-scrollbar :max-height="computedMaxHeight">
						<el-col style="margin-right: 10px;" :span="24" v-show="activeTab != '1' && activeTab != '2'">
							<ul>
								<li class="chat_listItem" v-for="item in syspromts">
									<el-row>
										<el-tooltip effect="dark" :content="item.content" placement="left">
											<el-row>
												<el-col :span="24" class="chat_listItem_title"><span>{{ item.title
														}}</span></el-col>
												<el-col :span="24" class="chat_listItem_content">
													<span>{{ item.content }}</span>
												</el-col>
											</el-row>

										</el-tooltip>
									</el-row>
								</li>
							</ul>
						</el-col>
					</el-scrollbar>
				</el-row>
			</el-aside>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, computed,onMounted,onUnmounted  } from 'vue'

import { IHooksOptions } from '@/hooks/interface'
import { useCrud } from '@/hooks'
import Import from './import.vue'
import Edit from './edit.vue'
import Generator from './generator.vue'
import { useTableSyncApi } from '@/api/table'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useDownloadApi } from '@/api/generator'
import { ta } from 'element-plus/es/locale';
import { template } from 'xe-utils'

const commandCenterFlag = ref(true)
// 定义关闭方法
const closeCommandCenter = () => {
	// 关闭 Command
	commandCenterFlag.value = false;
};

interface Tab {
	name: string;
	label: string;
}

const activeTab = ref<string>('1'); // 初始活动Tab的name
const tabs = ref<Tab[]>([
	{ name: '1', label: '对话' },
	{ name: '2', label: '参数' },
	{ name: '3', label: '办公助理' },
	{ name: '4', label: 'More' },
	{ name: '5', label: 'Tab 4' },
	{ name: '6', label: 'Tab 5' },
	{ name: '7', label: 'Tab 6' },
]);
const visibleTabsCount = 4; // 可见Tabs的数量
const tabOffset = ref<number>(0); // Tabs滚动的偏移量
// 模型对话数据
const chat_model = ref({})
// 参数
const parmars = ref({
	temperature: 0.5,
	top_p: 0.9,
	n_choices: 1,
	max_context: 8197,
	max_generations: 89000,
	presence_penalty: 0,
	frequency_penalty: 0,
	logit_bias: ''
})
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
const selectMode = ref({})

const visible = ref(false)

// 处理Tab点击事件（这里可以扩展为需要的逻辑）
const handleTabClick = (tab: any, ev: Event) => {
	// 点击最后一个向右移动
	if (tab.props.name == visibleTabs.value[visibleTabs.value.length - 1].name) {
		scrollRight()
	}
	// 点击第一个向前移动
	if (tab.props.name == visibleTabs.value[0].name) {
		scrollLeft()
	}
};

// 处理下拉菜单命令
const handleDropdownCommand = (command: number) => {
	tabOffset.value = command;
	activeTab.value = tabs.value[command].name
};

// 计算可见Tabs
const visibleTabs = computed(() => tabs.value.slice(tabOffset.value, tabOffset.value + visibleTabsCount));


// 滚动到左边的Tab
const scrollLeft = () => {
	if (tabOffset.value > 0) {
		tabOffset.value--;
	}
};

// 滚动到右边的Tab
const scrollRight = () => {
	if (tabOffset.value + visibleTabsCount < tabs.value.length + (tabs.value.length > visibleTabsCount ? 1 : 0)) {
		tabOffset.value++;
	}
};

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

// 点击空白关闭历史记录菜单
const closeHistoryMounted= onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

const closeHistoryUnmounted=  onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
 
const handleClickOutside = (event:any) => {
  modes.value.forEach(item => {
    if (!event.target.closest('.el-popover')) {
		closeHistoryMenu()
    }
  });
};
const state: IHooksOptions = reactive({
	dataListUrl: '/gen/table/page',
	deleteUrl: '/gen/table',
	queryForm: {
		tableName: ''
	}
})

const importRef = ref()
const editRef = ref()
const generatorRef = ref()

const importHandle = (id?: number) => {
	importRef.value.init(id)
}

const editHandle = (id?: number) => {
	editRef.value.init(id)
}

const generatorHandle = (id?: number) => {
	generatorRef.value.init(id)
}

const downloadBatchHandle = () => {
	const tableIds = state.dataListSelections ? state.dataListSelections : []

	if (tableIds.length === 0) {
		ElMessage.warning('请选择生成代码的表')
		return
	}

	useDownloadApi(tableIds)
}

const syncHandle = (row: any) => {
	ElMessageBox.confirm(`确定同步数据表${row.tableName}吗?`, '提示', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning'
	})
		.then(() => {
			useTableSyncApi(row.id).then(() => {
				ElMessage.success('同步成功')
			})
		})
		.catch(() => { })
}

const { getDataList, selectionChangeHandle, sizeChangeHandle, currentChangeHandle, deleteBatchHandle } = useCrud(state)
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
		margin-left:8px;
	}
}

.history-menu-item:hover {
	background: #f7f8fc
}

.history-menu>div:last-of-type {
	border-top: 1px solid #e8eaf2;
	color: #e63224;
}

</style>
