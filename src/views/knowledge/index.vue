<template>
    <el-card class="chat_card" body-style="padding: 0px;">

        <div class="chat_card_main">
            <div>
                <el-row :gutter="10">
                    <el-col :span="16">
                        <el-input v-model="search" placeholder="搜索知识库"></el-input>
                    </el-col>
                    <el-col :span="8">
                        <el-button title="新建" color="#567bff" @click="handleAdd">
                            <template #icon>
                                <svg-icon icon="icon-add"></svg-icon>
                            </template>
                            新建
                        </el-button>
                    </el-col>
                </el-row>
            </div>
            <KnowledgeAdd ref="knowledgeAddRef" />
        </div>

    </el-card>
</template>

<script setup lang="ts">
import { debounce } from 'lodash';
import { ref, onMounted } from 'vue'
import KnowledgeAdd from '@/views/knowledge/knowledgeAdd.vue'
const search = ref('')
const knowledgeAddRef = ref()

const handleAdd= ()=>{
    knowledgeAddRef.value.init()
}
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
</style>