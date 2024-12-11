<template>
    <el-select :teleported="false" v-model="model" v-bind="$attrs" placeholder="请选择模型">
        <el-option-group v-for="item in modelList" :key="item.group" :label="item.group">
            <el-tooltip v-for="data in item.options" :content="data.description" placement="right">
                <el-option :key="data.label" :label="data.label" :value="data.label">
                </el-option>
            </el-tooltip>
        </el-option-group>
    </el-select>


</template>

<script setup lang="ts">
import {ref,onMounted} from 'vue'
import { useModelsApi} from '@/api/chat'

// 当前模型
const model = defineModel<string>()

// 模型列表
const modelList = ref([])

const mounted = onMounted(() => {
	// 获取所有的模型
	getModelList();
});

// 获取所有的模型
const getModelList = () => {
	useModelsApi().then(res => {
		modelList.value = groupedModels(res)
	})
}

// 模型按照类别分类
const groupedModels = (dataList: any[]) => {
	return dataList.reduce((acc, model) => {
		const existingGroup = acc.find(g => g.group === model.model_type);
		if (existingGroup) {
			existingGroup.options.push({ label: model.label, description: model.description,default: model.default });
		} else {
			acc.push({
				group: model.model_type,
				options: [{ label: model.label, description: model.description,default: model.default }]
			});
		}
		return acc;
	}, []);	
}



</script>