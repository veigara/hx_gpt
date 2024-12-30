<template>
	<el-select :teleported="false" v-model="Knowledge" v-bind="$attrs" placeholder="请选择知识库" clearable>
		<el-tooltip v-for="item in KnowledgeList" :content="item.description" placement="right">
			<el-option :key="item.id" :label="item.know_name" :value="item.id" />
		</el-tooltip>
	</el-select>


</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useKnowledgeSearchApi } from '@/api/knowledge'

// 当前知识库
const Knowledge = defineModel<string>()

// 知识库列表
const KnowledgeList = ref([])

const mounted = onMounted(() => {
	// 获取所有的知识库
	getKnowledgeList();
});

// 获取所有的知识库
const getKnowledgeList = () => {
	useKnowledgeSearchApi({}).then(res => {
		KnowledgeList.value = res.data
	})
}
</script>