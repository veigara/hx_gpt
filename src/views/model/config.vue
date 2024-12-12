<template>
    <el-dialog v-model="visible" title="项目配置" :close-on-click-modal="false" append-to-body>
        <el-form :model="form" label-width="auto">
            <el-form-item label="Groq API Key" prop="groq_api_key">
                <el-input v-model="form.groq_api_key" placeholder="请输入Groq API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="LMStudio Host" prop="lmstudio_host">
                <el-input v-model="form.lmstudio_host" placeholder="请输入LMStudio Host" clearable></el-input>
            </el-form-item>
            <el-form-item label="LMStudio API Key" prop="lmstudio_api_key">
                <el-input v-model="form.lmstudio_api_key" placeholder="请输入LMStudio API Key" clearable></el-input>
            </el-form-item>
            <el-form-item label="默认模型" prop="default_model">
                <mode-select v-model="form.default_model" style="width: 100%;" />
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
    lmstudio_host: '',
    lmstudio_api_key: '',
    default_model: ''
}
const form = reactive({
    ...formData
})

const clearForm = () => {
    Object.assign(form, formData)
}
// 获取配置
const getConfig = () => {
    useGetConfigApi().then(data => {
        form.groq_api_key = data.groq_api_key
        form.lmstudio_host = data.lmstudio_host
        form.lmstudio_api_key = data.lmstudio_api_key
        form.default_model = data.default_model
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

defineExpose({
    init
})

</script>

<style lang="scss" scoped></style>