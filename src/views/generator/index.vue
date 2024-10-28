<template>
	<el-card class="chat_card" body-style="padding: 0px;">
		<el-container>
			<el-aside width="260px" class="chat_card_aside">Aside</el-aside>
			<el-main class="chat_card_main"></el-main>
			<el-aside width="260px" class="chat_card_aside" v-if="commandCenterFlag">
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
						<el-dropdown @click="handleDropdownCommand">
							<div style="cursor: pointer;"> <svg-icon icon="icon-menu"></svg-icon></div>
							<template #dropdown>
								<el-dropdown-menu>
									<el-dropdown-item v-for="tab in tabs" :key="tab.name">{{ tab.label
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
								<div style="font-size: 16px;font-weight: 600;color: #000;">
									System prompt
								</div>
								<el-input clearable type="textarea" :rows="5" placeholder="System prompt" />
							</el-collapse-item>
							<el-collapse-item title="知识库" name="3">
								<div>
									<el-upload class="upload-demo" drag
										action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" multiple>
										<svg-icon icon="icon-cloud-upload" style="font-size: 50px;"><upload-filled /></svg-icon>
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
				</el-row>
			</el-aside>
		</el-container>
	</el-card>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'



import { IHooksOptions } from '@/hooks/interface'
import { useCrud } from '@/hooks'
import Import from './import.vue'
import Edit from './edit.vue'
import Generator from './generator.vue'
import { useTableSyncApi } from '@/api/table'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useDownloadApi } from '@/api/generator'
import { ta } from 'element-plus/es/locale';

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
const visibleTabsCount = 3; // 可见Tabs的数量
const tabOffset = ref<number>(0); // Tabs滚动的偏移量
// 模型对话数据
const chat_model = ref({})


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
const handleDropdownCommand = (command: string) => {
	activeTab.value = command;

};

// 计算可见Tabs
const visibleTabs = computed(() => tabs.value.slice(tabOffset.value, tabOffset.value + visibleTabsCount));

// 计算隐藏Tabs（除了可见Tabs和More Tab之外的Tabs）
const hiddenTabs = computed(() => {
	const allTabsExceptMore = tabs.value.filter(tab => tab.name !== 'more');
	return allTabsExceptMore.slice(0, tabOffset.value).concat(allTabsExceptMore.slice(tabOffset.value + visibleTabsCount));
});

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
	padding: 24px 8px 8px 8px;
	border-right: 1px solid rgba(237, 239, 245, .45);
	min-height: calc(100vh - 19px);
}

.chat_card_main {
	background-color: rgb(246, 247, 251);
	min-height: calc(100vh - 19px);
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
	background: rgb(247, 248, 252);
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
</style>
