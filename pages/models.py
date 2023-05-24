from django.db import models


# Create your models here.
class Tool(models.Model):
    tool_name = models.CharField(max_length=255, verbose_name="工具名称", default="")
    tool_class = models.IntegerField(verbose_name="工具类型")
    # 廉价工具为1 贵重物品为2
    tool_price = models.FloatField(verbose_name="工具价格")
    tool_part = models.IntegerField(verbose_name="工具所属部门")
    tool_area = models.IntegerField(verbose_name="工具所属区域")
    tool_borrowed = models.BooleanField(default=False, verbose_name="工具是否被借出")
    tool_damaged = models.BooleanField(default=False, verbose_name="工具是否损坏")
