from django.db import models


class AiHistory(models.Model):
    # 模型中不需要指定id
    # 数据库可变类型
    title = models.CharField("聊天记录名称", max_length=200)
    content = models.TextField("聊天记录内容(json字符串)")
    agent_id = models.CharField("角色体id", max_length=200)
    all_token_counts = models.BigIntegerField("当前记录token数")
    count = models.IntegerField("当前对话数")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间")
    user_name = models.CharField("用户名", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "ai_history"
        verbose_name = "聊天记录"
        verbose_name_plural = verbose_name
