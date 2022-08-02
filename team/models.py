from django.db import models
# Create your models here.
from django.db import models
import datetime


# Create your models here.
class Team(models.Model):
    team_id = models.AutoField(verbose_name="团队ID", unique=True, primary_key=True)
    team_name = models.CharField(max_length=50, verbose_name="团队名称")
    establisher = models.CharField(max_length=128, verbose_name="创始人用户名")
    establish_time = models.DateTimeField(max_length=80, verbose_name="团队成立时间")
    member_num = models.IntegerField(verbose_name="成员数", default=1)
    project_num = models.IntegerField(verbose_name="项目数", default=0)
