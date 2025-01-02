from django.db import models


class AiAgent(models.Model):
    # 模型中不需要指定id
    # 数据库可变类型
    title = models.CharField("智能体名称", max_length=200)
    content = models.TextField("智能体内容(json字符串)", max_length=200)
    model_key = models.CharField("模型名称", max_length=200)
    temperature = models.CharField("随机性", max_length=200)
    top_p = models.CharField("核采样", max_length=200)
    max_tokens = models.BigIntegerField("单次交互所用的最大Token数")
    presence_penalty = models.CharField("核采样", max_length=200)
    top_p = models.CharField("话题新鲜度", max_length=200)
    frequency_penalty = models.CharField("频率惩罚度", max_length=200)
    user_icon = models.CharField("用户图标", max_length=200)
    assistant_icon = models.CharField("助理图标", max_length=200)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间")
    user_name = models.CharField("用户名", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "ai_agent"
        verbose_name = "智能体"
        verbose_name_plural = verbose_name
