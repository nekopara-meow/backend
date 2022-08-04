
from django.db import models
import datetime


# Create your models here.
class Team(models.Model):
    team_id = models.AutoField(verbose_name="团队ID", unique=True, primary_key=True)
    team_name = models.CharField(max_length=50, verbose_name="团队名称")
    brief_intro = models.CharField(max_length=1024, default="这个团队很懒，什么也没写")
    creator = models.CharField(max_length=128, verbose_name="创始人用户名")
    create_time = models.DateTimeField(max_length=80, verbose_name="团队成立时间", auto_now_add=True)
    member_num = models.IntegerField(verbose_name="成员数", default=1)
    project_num = models.IntegerField(verbose_name="项目数", default=0)
    avatar = models.CharField(max_length=255, default="https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/yonghutouxiang/Transparent_Akkarin.jpg")

class Uml(models.Model):
    team_id = models.IntegerField
    creator = models.CharField(max_length=128)
    uml_id = models.AutoField(primary_key=True)
    uml_url = models.CharField(max_length=1024)
