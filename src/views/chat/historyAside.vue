<template>
	<el-row>
		<el-input v-model="props.searchTxt" placeholder="搜索历史记录" style="border-radius: 20px;">
			<template #prefix>
				<svg-icon icon="icon-search"></svg-icon>
			</template>
		</el-input>
	</el-row>
	<div style="overflow: hidden;margin-top:20px">
		<el-scrollbar :max-height="computedHistoryMaxHeight">
			<ul>
				<li  :class="{'history_listItem':true, 'history_listItem_active':item.active ==true }"
					v-for="item in props.historys" :key="item.id" @click="selectHistoryItem(item)">
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
</template>

<script setup lang="ts">
import { nextTick, reactive, ref,computed,onMounted,onUnmounted } from 'vue'


interface Props {
  // 搜索文本
  searchTxt?: string
  // 计算历史记录最大高度
  historys:any
  // 保存点击的记录
  selectedHistory:string
}

const props = defineProps<Props>()

// 点击历史记录 
const selectHistoryItem = (item: any) => {
	// 其他取消
	props.historys.filter(item => item.active ==true).find(item => item.active = false)	
	// 指定当前
	item.active = true
	props.selectedHistory = item
}

// 左边历史记录
// 右边其他参数
const themeHeaderHeight = ref(window.getComputedStyle(document.documentElement).getPropertyValue('--theme-header-height'));
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
	props.historys.filter(item => item.show == true).find(item => item.show = false)
}

const mounted = onMounted(() => {
	// 点击空白关闭历史记录菜单
	document.addEventListener('click', handleClickOutside);
});

const closeHistoryUnmounted = onUnmounted(() => {
	document.removeEventListener('click', handleClickOutside);
});

const handleClickOutside = (event: any) => {
	props.historys.forEach(item => {
		if (!event.target.closest('.el-popover')) {
			closeHistoryMenu()
		}
	});
};
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
</style>
