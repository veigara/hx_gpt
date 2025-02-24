<template>
	<el-dialog v-model="visible" title="功能面板" :close-on-click-modal="false" append-to-body>
		<div>
			<ul class="infinite-list" style="overflow: auto">
				<li @click="clearContxt">清空当前聊天记录</li>
				<li @click="clearAllHistory">清空所有聊天记录</li>
			</ul>
		</div>
		<template #footer>
			<el-button @click="visible = false">取消</el-button>
		</template>
	</el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import { useClearHistoryContextApi, useClearHistoryAllApi } from '@/api/chat'

const props = defineProps({
	historyId: {
		type: String,
		default: false
	}
})
const visible = ref(false)
const emit = defineEmits(['clear_all_history','refresh_history'])

const init = () => {
	visible.value = true
}

// 清空上下文
const clearContxt = () => {
	if(!props.historyId || props.historyId ==''){
		return ElNotification({
			title: '失败',
			message: '请选择要清空的聊天记录',
			type: 'error'
		})
	}
	useClearHistoryContextApi({
		id: props.historyId
	}).then(res => {
		visible.value = false
		// 重新加载聊天数据
		emit('refresh_history')
		ElNotification({
			title: '成功',
			message: '清空上下文成功',
			type: 'success'
		})
	})
}

// 清空所有聊天记录
const clearAllHistory = () => {
	ElMessageBox.confirm(
		'是否确认删除所有记录？此操作不可恢复',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			useClearHistoryAllApi().then(res => {
				ElNotification({
					title: '成功',
					message: '清空所有聊天记录成功',
					type: 'success'
				})
				visible.value = false
				emit('clear_all_history')
			})
		})
}

defineExpose({
	init
})
</script>

<style lang="scss" scoped>
.infinite-list {
	padding: 0;
	margin: 0;
	list-style: none;

	li {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 50px;
		margin: 10px;
		border: 1px solid rgba(0, 0, 0, 0.1);
		cursor: pointer;
	}

	li:hover {
		background: var(--el-color-primary-light-9);
		color: var(--el-color-primary);
	}
}
</style>
