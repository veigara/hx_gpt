<template>
    <el-card class="chat_card" body-style="padding: 0px;">

        <div class="chat_card_main">
            <div>
                <el-row :gutter="10">
                    <el-col :span="16">
                        <el-input v-model="search" placeholder="搜索模型" clearable></el-input>
                    </el-col>
                    <el-col :span="8">
						<el-button :icon="Search" circle @click="getModelList" />
                        <el-button title="新建" color="#567bff" @click="handleAdd">
                            <template #icon>
                                <svg-icon icon="icon-add"></svg-icon>
                            </template>
                            新建
                        </el-button>
						<el-button title="项目配置" color="#567bff" @click="openProjectConf">
                            <template #icon>
                                <svg-icon icon="icon-wrench"></svg-icon>
                            </template>
                            项目配置
                        </el-button>
                    </el-col>
                </el-row>
            </div>
            <div class="model">
                <div v-for="item in modelList" :key="item.model_key" class="model_item">
				<div class="model_header">
					<div class="model_icon"></div>
					<div>
						<div class="model_title">{{ item.model_key }}</div>
						<div class="model_info">模型类别: {{ item.model_type }}</div>
						<div class="model_info" v-if="item.max_content_len">最大上下文长度: {{ item.max_content_len }} tokens</div>
                        <div class="model_info" v-if="item.multimodal"><span style="color:blue;">视觉模型:能处理图像输入</span></div>
                        <div class="model_info">描述：{{ item.description }}</div>
                    </div>
				</div>
				<div class="model_action">
					<el-button title="查看" type="info" text @click="handview(item)">
						<template #icon>
							<svg-icon icon="icon-view"></svg-icon>
						</template>
						查看
					</el-button>
					<el-button title="删除" :icon="Delete" type="danger" text @click="delview(item)">
						删除
					</el-button>
				</div>
			</div>
            </div>
        </div>
		<ModelAdd ref="modelAddRef" @submit="getModelList"></ModelAdd>
		<ProjectConfig ref="projectConfigRef" ></ProjectConfig>
    </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAllModelsApi,useRemoveModelApi} from '@/api/model'
import ModelAdd from '@/views/model/modelAdd.vue'
import ProjectConfig from '@/views/model/config.vue'
import { ElMessage, ElMessageBox } from 'element-plus/es'
import { Delete,Search } from '@element-plus/icons-vue'

const modelList = ref([])
const search = ref()
const modelAddRef = ref()
const projectConfigRef = ref()

// 获取所有的模型
const getModelList =() =>{  
    const data = {
        keyword:search.value
    }
    useAllModelsApi(data).then(res => {
        modelList.value = res.data
    })
}

// 新建
const handleAdd = () => {
    modelAddRef.value.init(false)
}

// 修改
const handview = (item:any) => {
	modelAddRef.value.init(true,item)
}

// 删除
const delview = (item:any) => {
	ElMessageBox.confirm(
		'是否确认删除该模型？',
		'警告',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			useRemoveModelApi({ "id": item.id }).then(res => {
				ElMessage.success('删除成功')
				// 刷新列表
				getModelList()
			})
		})
}

// 打开项目配置
const openProjectConf = () => {
    projectConfigRef.value.init()
}

onMounted(() => {
    getModelList()
})

</script>

<style lang="scss" scoped>
.chat_card {
    .el-card {
        border: none !important;
    }
}

.chat_card_main {
    background-color: rgb(255, 255, 255);
    min-height: calc(100vh - 59px);
    margin: 0px auto;
    max-width: 896px;
    min-width:320px;
    padding: 20px;
}


.model {
	padding: 20px 0px;
}

.model_item {
	display: flex;
	justify-content: space-between;
	padding: 20px;
	border: 1px solid #dedede;
}

.model_item:not(:last-child) {
	border-bottom: 0px;
}

.model_item:first-child {
	border-top-left-radius: 10px;
	border-top-right-radius: 10px;
}

.model_item:last-child {
	border-bottom-left-radius: 10px;
	border-bottom-right-radius: 10px;
}

.model_header {
	display: flex;
	align-items: center;
	max-width: 700px;
	.model_icon {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 10px;
	}

	.model_title {
		font-size: 14px;
		font-weight: 700;
	}

	.model_info {
		font-size: 12px;
		white-space: normal;
		word-wrap: break-word;
		overflow-wrap: break-word;
		max-width: 100%;
	}
}

.model_action {
	display: flex;
	flex-wrap: nowrap;
}
</style>