from django.db import models
# Create your models here.
from django.db import models
import datetime


# Create your models here.
class Projectt(models.Model):
    team_id = models.IntegerField(verbose_name="项目所属团队ID")
    project_id = models.AutoField(verbose_name="项目ID", primary_key=True)
    project_name = models.CharField(max_length=50, verbose_name="项目名称")
    creator = models.CharField(max_length=128, verbose_name="创始人用户名")
    create_time = models.DateTimeField(max_length=80, verbose_name="项目成立时间", auto_now_add=True)
    brief_intro = models.CharField(max_length=1024, default="我不到啊")


class File(models.Model):
    project_id = models.IntegerField(verbose_name="文件所属项目ID")
    file_name = models.CharField(max_length=128)
    file_type = models.IntegerField(verbose_name="文件种类")
    creator = models.CharField(max_length=128)
    file_id = models.AutoField(primary_key=True)
    file_url = models.CharField(max_length=1024)

