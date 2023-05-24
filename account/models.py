from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Employee(models.Model):
    em_classes = models.IntegerField(verbose_name="职员类型")
    em_belong = models.IntegerField(verbose_name="职员所属部门")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
