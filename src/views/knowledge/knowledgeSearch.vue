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
                    <el-button v-if="streamLoading" color="#ff0000" @click="abortRequest">停止</el-button>
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
import { fetchEventSource } from '@microsoft/fetch-event-source'


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
// 流
const streamLoading = ref(false)
// 
const knowKey = ref(true)

let abortController = null
// 检索
const search = () => {
    if(!checkParms()){
        return
    };
    isLoading.value = true
    streamLoading.value = true
    answer.value = ''

    const fetchStream = async (dataForm: any) => {
		abortController = new AbortController()
		try {
            const url = import.meta.env.VITE_API_URL as any
            const user = import.meta.env.VITE_USER_AUTHORIZATION as any
			await fetchEventSource(url+'/knowledge/retrieve', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', 'authorization': user },
				body: JSON.stringify(dataForm),
				signal: abortController.signal, // 绑定中断信号
				onopen: async (response) => {
					isLoading.value = true
                    streamLoading.value = true
                    if (response.status !== 200) {
                        // 主动读取错误流
                        const errorData = await response.json(); 
                        throw new Error(errorData.error || '请求失败');
                    }
				},
				onmessage: (e) => {
					const datas = e.data.replace('[TEXT]', '').replace('[/TEXT]', '').replace(/<br>/g, '\n\n')// 转换换行符为HTML
					datas.split('').forEach((char, index) => {
						setTimeout(() => {
							answer.value += char, 50 * index
							isLoading.value = false
						})
					})

				},
				onclose: () => {
					isLoading.value = false
                    streamLoading.value = false
				},
				onerror: (err) => {
                    // 禁用重试
                    throw err
				}
			})
		} catch (error) {
			console.error('请求失败:', error)
			if (error.name === 'AbortError') {
				console.log('请求已被中止')
				answer.value = "请求已被中止"
			} else {
				answer.value = "请求失败："+error.message
			}
			isLoading.value = false
            streamLoading.value = false
		} finally {
			abortController = null
		}

	}

	fetchStream(queryForm)
}

// 中断请求方法
const abortRequest = () => {
  if (abortController) {
    abortController.abort() // 触发中止
	answer.value += "\n\n 请求已被中止"
    isLoading.value = false
    abortController = null
  }
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