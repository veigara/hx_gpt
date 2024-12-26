<template>
    <el-card class="chat_card" body-style="padding: 0px;">

        <div class="chat_card_main">
            <el-tabs v-model="activeName" type="border-card" class="know-tabs">
                <el-tab-pane label="知识库管理" name="first">
                    <div>
                        <el-row :gutter="10">
                            <el-col :span="16">
                                <el-input v-model="search" placeholder="搜索知识库"></el-input>
                            </el-col>
                            <el-col :span="8">
                                <el-button :icon="Search" circle />
                                <el-button title="新建" color="#567bff" @click="handleAdd">
                                    <template #icon>
                                        <svg-icon icon="icon-add"></svg-icon>
                                    </template>
                                    新建
                                </el-button>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="model">
                        <div v-for="item in dataList" :key="item.id" class="model_item">
                            <div class="model_header">
                                <div class="model_icon"></div>
                                <div>
                                    <div class="model_title">{{ item.know_name }}</div>
                                    <div class="model_info">索引：{{ item.index_name }}</div>
                                    <div class="model_info">描述：{{ item.description }}</div>
                                    <div class="model_info">创建时间: {{ item.create_time }}</div>
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
                    <KnowledgeAdd ref="knowledgeAddRef" @submit="loadData" />
                </el-tab-pane>
                <el-tab-pane label="检索知识库" name="second">检索中</el-tab-pane>
            </el-tabs>


        </div>        
    </el-card>
</template>

<script setup lang="ts">
import { Delete } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'
import KnowledgeAdd from '@/views/knowledge/knowledgeAdd.vue'
import { useKnowledgeSearchApi, useKnowledgeDelApi } from '@/api/knowledge'
import { ElMessage, ElMessageBox } from 'element-plus/es'
import { Search } from '@element-plus/icons-vue'


const search = ref('')
const dataList = ref([])
const knowledgeAddRef = ref()
const activeName = ref('first')
const handleAdd = () => {
    knowledgeAddRef.value.init()
}

const loadData = () => {
    const query = {
        know_name: search.value
    }
    useKnowledgeSearchApi(query).then(res => {
        dataList.value = res.data
    })
}

// 查看
const handview = (item: any) => {
    knowledgeAddRef.value.init(item)
}

// 删除
const delview = (item: any) => {
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
            useKnowledgeDelApi({ "id": item.id }).then(res => {
                ElMessage.success('删除成功')
                // 刷新列表
                loadData()
            })
        })
}

onMounted(() => {
    loadData()
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
    min-width: 320px;
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

.know-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}
</style>