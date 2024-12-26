from django.db import models


class Knowledge(models.Model):
    # 模型中不需要指定id
    # 数据库可变类型
    know_name = models.CharField("know_name", max_length=200)
    index_name = models.CharField("索引名称", max_length=200)
    description = models.CharField("描述", max_length=200)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间")
    user_name = models.CharField("用户名", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "knowledge"
        verbose_name = "知识库"
        verbose_name_plural = verbose_name
