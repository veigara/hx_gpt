<template>
    <div style="min-height: calc(100vh - 130px);">
        <el-progress v-if="isLoading" :percentage="100" :indeterminate="true" :show-text="false" striped/>
        <div class="query_container">
            <div class="query_item">
                <div class="query_item_label"> 模型</div>
                <div class="query_item_content">
                    <mode-select v-model="queryForm.model_name" />
                </div>
            </div>
            <div class="query_item">
                <div class="query_item_label"> 知识库</div>
                <div class="query_item_content">
                    <knowledge-select v-if="knowKey"  v-model="queryForm.know_id" />
                </div>
            </div>
        </div>
        <div class="query_container">
            <el-row :gutter="20" style="margin-bottom: 5px;">
                <el-col :span="16">
                    <el-input v-model="queryForm.search_text" placeholder="请输入检索内容" clearable  @keyup.enter="search" />
                </el-col>
                <el-col :span="8">
                    <el-button v-if="isLoading" color="#ff0000" disabled>加载中</el-button>
                    <el-button v-else type="primary" @click="search">检索</el-button>
                </el-col>
            </el-row>
        </div>
        <div class="answer_container">
            <TextComponent ref="textRef" :text="answer" :loading="false"
											:asRawText="false" />
        </div>

    </div>

</template>

<script setup lang="ts">
import ModeSelect from '@/components/model-select/index.vue'
import knowledgeSelect from '@/components/knowledge-select/index.vue'
import TextComponent from '@/components/Message/Text.vue'
import { ref, reactive } from 'vue'
import { useKnowledRetrievetApi } from '@/api/knowledge'
import { ElNotification } from 'element-plus'


const inintData = () => {
    return {
        model_name: '',
        know_id: '',
        search_text: ''
    }
}

const queryForm = reactive({ ...inintData })
// 回答
const answer = ref<any>()
// 加载中
const isLoading = ref(false)
// 
const knowKey = ref(true)
// 检索
const search = () => {
    if(!checkParms()){
        return
    };
    isLoading.value = true
    answer.value = ''
    useKnowledRetrievetApi(queryForm).then(res => {
        answer.value = res.data
        isLoading.value = false
    }).catch(err => {
        isLoading.value = false
    })
}

const checkParms = () => {
    if (!queryForm.model_name) {
        ElNotification({
            title: '提示',
            message: '请选择模型',
            type: 'warning',
        })
        return false
    }
    if (!queryForm.know_id) {
        ElNotification({
            title: '提示',
            message: '请选择知识库',
            type: 'warning',
        })
        return false
    }
    if (!queryForm.search_text) {
        ElNotification({
            title: '提示',
            message: '请输入检索内容',
            type: 'warning',
        })
        return false
    }

    return true
}    

const init = () => {
    Object.assign(queryForm, inintData())
    knowKey.value = true
}

const isRefreshKonw = (flag:boolean) => {
    knowKey.value = flag
}

defineExpose({
    init,
    isRefreshKonw
})

</script>


<style lang="scss" scoped>
.query_container {
    margin-bottom: 10px;
}

.query_item {
    display: inline-flex;
    margin-bottom: 10px;
    margin-right: 20px;

    .query_item_label {
        line-height: 32px;
        height: 32px;
        margin-right: 10px;
    }

    .query_item_content {
        align-items: center;
        line-height: 32px;
    }
}
</style>