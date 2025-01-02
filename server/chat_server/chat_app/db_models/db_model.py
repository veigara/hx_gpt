from django.db import models


class AiModel(models.Model):
    # 模型中不需要指定id
    # 数据库可变类型
    model_key = models.CharField("调用模型主键", max_length=200)
    model_name = models.CharField("模型显示名称", max_length=200)
    description = models.CharField("描述", max_length=200)
    model_type = models.CharField("模型类型", max_length=200)
    multimodal = models.BooleanField("是否多模态", default=False)
    max_content_len = models.BigIntegerField("模型支持的最大上下文长度")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间")
    user_name = models.CharField("用户名", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "ai_model"
        verbose_name = "模型配置"
        verbose_name_plural = verbose_name
