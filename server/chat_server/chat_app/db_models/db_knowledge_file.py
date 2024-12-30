from django.db import models


class KnowledgeFile(models.Model):
    # 模型中不需要指定id
    # 数据库可变类型
    knowledge_id = models.CharField("知识库ID", max_length=64)
    title = models.CharField("文件标题", max_length=200)
    file_id = models.CharField("文件名", max_length=200)
    file_type = models.CharField("文件类型", max_length=50)
    file_size = models.CharField("文件大小(兆)", max_length=200)
    file_path = models.CharField("文件路径(绝对路径)", max_length=255)
    file_index_name = models.CharField("向量文件索引名", max_length=255)
    file_index_ids = models.TextField("向量文件索引ID,用逗号分隔")
    docment_count = models.IntegerField("文档数量")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间")
    user_name = models.CharField("用户名", max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "knowledge_file"
        verbose_name = "知识库文件"
        verbose_name_plural = verbose_name
