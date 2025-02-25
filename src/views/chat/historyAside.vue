<template>
	<el-row :gutter="1">
		<el-col :span="20">
			<el-input v-model="searchTxt" placeholder="搜索聊天记录" style="border-radius: 20px;"
				@input="debouncedSearchTitle">
				<template #prefix>
					<svg-icon icon="icon-search"></svg-icon>
				</template>
			</el-input>
		</el-col>
		<el-col :span="2">
			<div class="add-chat" title="新建对话" @click="addChat">
				<el-icon :size="20">
					<Plus />
				</el-icon>
			</div>
		</el-col>
		<el-col :span="2">
			<div class="add-chat" title="刷新" @click="refreshChat">
				<el-icon :size="20">
					<Refresh />
				</el-icon>
			</div>
		</el-col>		
	</el-row>
	<div style="overflow: hidden;margin-top:20px">
		<el-scrollbar :max-height="computedHistoryMaxHeight">
			<ul>
				<li :class="{ 'history_listItem': true, 'history_listItem_active': item.active == true }"
					v-for="item in historys" :key="item.id" @click="selectHistoryItem(item)">
					<div style="width: 100%;padding: 0px 10px 0px 0px;">						
						<el-tooltip
							effect="dark"
							:content="item.title"
							placement="right"
						>
						<div><span class="history_listItem_content">{{ item.title }}</span></div>
						</el-tooltip>
						<div style="display: flex;justify-content: space-between;font-size: 12px;color: #a6a6a6;">
							<div class="history_listItem_time">共{{ item.count }}条对话</div>
							<div class="history_listItem_time">{{ item.create_time }}</div>
						</div>
					</div>
					<el-popover :visible="item.show == true" placement="right-start" :show-arrow="false"
						style="padding: 0px;">
						<div class="history-menu">
							<div class="history-menu-item" @click="showRenameInput(item)">
								<span><svg-icon icon="icon-edit" /></span>重命名
							</div>
							<div class="history-menu-item" @click="topHistory(item)">
								<span><svg-icon icon="icon-add-top" /></span>置顶此对话
							</div>
							
							<div class="history-menu-item">
								<span><svg-icon icon="icon-agent" /></span>转为智能体
							</div>
							<div class="history-menu-item" @click="delHistory(item)">
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
</template>

<script setup lang="ts">
import { nextTick, reactive, ref, computed, onMounted, onUnmounted } from 'vue'
import { useGetHistorysApi, useRenameHistoryApi, useDelHistoryApi, useTopHistoryApi } from '@/api/chat'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus,Refresh } from '@element-plus/icons-vue'
import { debounce } from 'lodash';

const historys = ref<any>([])
// 搜索聊天记录
const searchTxt = ref()

const emits = defineEmits(['click:history', 'refresh:history'])
// 获取用户聊天记录
const getUserHistory = () => {
	useGetHistorysApi({ "keyword": searchTxt.value }).then(res => {
		historys.value = res.data
	})
}

// 设置记录为激活状态
const activeHistoryItem = (historyId: String) => {
	useGetHistorysApi({ "keyword": searchTxt.value }).then(res => {
		historys.value = res.data
		historys.value.find(item => item.id == historyId).active = true
	})
}

// 新建后刷新列表后点击第一个数据
const refreshAndSelectFirstHistory = (isClearChat: boolean) => {
	// 刷新聊天记录
	useGetHistorysApi({ "keyword": searchTxt.value }).then(res => {
		historys.value = res.data
		if (res && res.data && res.data.length > 0) {
			// 激活第一个
			historys.value[0].active = true
			emits('click:history', { historyId: historys.value[0].id, isClearChat: isClearChat })
		}
	})
}

// 取消所有选中
const clearAll = () => {
	searchTxt.value = ''
	getUserHistory()
}

// 设置聊天记录条数
const setHistoryCount=(historyId:string,num: number) =>{
	historys.value.find(item => item.id == historyId).count = num
}

defineExpose({
	activeHistoryItem,
	refreshAndSelectFirstHistory,
	clearAll,
	setHistoryCount
})

// 点击聊天记录 
const selectHistoryItem = (item: any) => {
	// 其他取消
	historys.value.filter(item => item.active == true).find(item => item.active = false)
	// 指定当前
	item.active = true
	// 将聊天记录id给父组件
	emits('click:history', { historyId: item.id, isClearChat: true })
}

// 左边聊天记录
// 右边其他参数
//const themeHeaderHeight = ref(window.getComputedStyle(document.documentElement).getPropertyValue('--theme-header-height'));
// 计算最大高度
const computedHistoryMaxHeight = computed(() => {
	//const headerHeight = parseFloat(themeHeaderHeight.value);
	//return `calc(100vh - 19px - 90px - ${headerHeight}px)`;
	return `calc(100vh - 19px - 90px )`;
});

// 打开聊天记录的菜单
const openHistoryMenu = (item: any) => {
	// 其他菜单隐藏
	closeHistoryMenu()
	item.show = true;
}

// 关闭菜单
const closeHistoryMenu = () => {
	historys.value.filter(item => item.show == true).find(item => item.show = false)
}

const mounted = onMounted(() => {
	// 点击空白关闭聊天记录菜单
	document.addEventListener('click', handleClickOutside);
	getUserHistory()
});

const closeHistoryUnmounted = onUnmounted(() => {
	document.removeEventListener('click', handleClickOutside);
});

const handleClickOutside = (event: any) => {
	historys.value.forEach(item => {
		if (!event.target.closest('.el-popover')) {
			closeHistoryMenu()
		}
	});
};

// 重命名
const showRenameInput = (item: any) => {
	ElMessageBox.prompt('请输入聊天记录的标题', '重命名', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		inputPattern: /.+?/,
		inputErrorMessage: '标题不能为空',
	})
		.then(({ value }) => {
			useRenameHistoryApi({ id: item.id, new_title: value }).then(res => {
				// 刷新
				getUserHistory()
				ElMessage.success('重命名成功')
			})
		})
}

// 新建对话
const addChat = () => {
	// 页面上全部初始化,显示提示信息
	emits('refresh:history', true)
}

const delHistory = (item: any) => {
	ElMessageBox.confirm(
		'是否确认删除该对话记录？',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			// 删除聊天记录
			useDelHistoryApi({ id: item.id }).then(res => {
				// 刷新
				getUserHistory()
				ElMessage.success('删除成功')
				emits('refresh:history', false)
			})
		})

}

// 300ms 的防抖时间
const debouncedSearchTitle = debounce(getUserHistory, 300);

// 置顶对话
const topHistory = (item: any) => {
	useTopHistoryApi({ id: item.id }).then(res => {
		// 刷新
		getUserHistory()
		ElMessage.success('置顶成功')
	})
}

// 刷新对话
const refreshChat = () => {
	// 页面上全部初始化,显示提示信息
	emits('refresh:history', true)
}
</script>

<style lang="scss">
.history_listItem {
	align-items: center;
	border-radius: 12px;
	box-sizing: border-box;
	color: #26244c;
	cursor: pointer;
	display: flex;
	flex-shrink: 0;
	font-size: 14px;
	//height: 36px;
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
	white-space: nowrap;
	font-size: 14px;
	font-weight: bolder;
}

.history_listItem_icon {
	display: inline-block;
	height: 22px;
	line-height: 26px;
	margin-left: 2px
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

.add-chat {
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	cursor: pointer;
}
</style>
