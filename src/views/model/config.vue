<template>
    <el-dialog v-model="visible" title="项目配置" :close-on-click-modal="false" append-to-body>
        <el-form :model="form" label-width="auto" :rules="rules">
            <el-form-item label="Groq API Key" prop="groq_api_key">
                <el-input v-model="form.groq_api_key" placeholder="请输入Groq API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="千问API Key" prop="qwen_api_key">
                <el-input v-model="form.qwen_api_key" placeholder="请输入千问API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="讯飞API Key" prop="qwen_api_key">
                <el-input v-model="form.spark_api_key" placeholder="请输入讯飞API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="LMStudio url" prop="lmstudio_url">
                <el-input v-model="form.lmstudio_url" placeholder="请输入LMStudio Host" clearable></el-input>
            </el-form-item>
            <el-form-item label="LMStudio API Key" prop="lmstudio_api_key">
                <el-input v-model="form.lmstudio_api_key" placeholder="请输入LMStudio API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="默认模型" prop="default_model">
                <mode-select v-model="form.default_model" style="width: 100%;" />
            </el-form-item>
            <el-form-item label="向量数据库连接地址" prop="redis_url">
                <el-input v-model="form.redis_url" placeholder="向量数据库连接地址" clearable></el-input>
            </el-form-item>
            <el-form-item label="本地向量模型地址" prop="embedding">
                <el-input v-model="form.embedding" placeholder="本地向量模型地址" clearable></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="visible = false">取消</el-button>
            <el-button type="primary" @click="updateConfig">确定</el-button>
        </template>
    </el-dialog>

</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useGetConfigApi, useUpdateConfigApi } from '@/api/config'
import ModeSelect from '@/components/model-select/index.vue'
import { ElNotification } from 'element-plus'

const visible = ref(false)
const formData = {
    groq_api_key: '',
    lmstudio_url: '',
    lmstudio_api_key: '',
    default_model: '',
    qwen_api_key:'',
    spark_api_key:'',
    redis_url:'',
    embedding:''
}
const form = reactive({
    ...formData
})

const clearForm = () => {
    Object.assign(form, formData)
}
// 获取配置
const getConfig = () => {
    useGetConfigApi().then(res => {
        form.groq_api_key = res.data.groq_api_key
        form.lmstudio_url = res.data.lmstudio_url
        form.lmstudio_api_key = res.data.lmstudio_api_key
        form.default_model = res.data.default_model
        form.qwen_api_key = res.data.qwen_api_key
        form.spark_api_key = res.data.spark_api_key
        form.redis_url = res.data.redis_url
        form.embedding = res.data.embedding
    })

}

// 初始化
const init = () => {
    getConfig()
    visible.value = true
}

const updateConfig = () => {
    useUpdateConfigApi({data:form}).then(() => {
        visible.value = false
        ElNotification({
            title: '温馨提示',
            message: '修改配置成功',
            type: 'success'
        })
        clearForm()
    })
}

const rules = reactive({
	redis_url: [{ required: true, message: '向量数据库连接地址不能为空', trigger: 'blur' }],
	embedding: [
		{
			required: true,
			message: '本地向量模型地址不能为空',
			trigger: 'blur'
		}
	]
})

defineExpose({
    init
})

</script>

<style lang="scss" scoped></style>