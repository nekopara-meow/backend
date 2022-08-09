from django.db import models
# Create your models here.
from django.db import models
import datetime


# Create your models here.


class Member_in_Team(models.Model):
    username = models.CharField(max_length=128)
    team_id = models.IntegerField(verbose_name="团队ID")
    priority = models.IntegerField(verbose_name="该成员在该项目中权限等级")

    class Meta:
        indexes = [
            models.Index(fields=['username'], name='username_index')
        ]


class PersonalMessage(models.Model):
    sender = models.CharField(max_length=128, verbose_name="发送/操作者username")
    receiver = models.CharField(max_length=128, verbose_name="接收者username")
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")


class TeamMessage(models.Model):
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    sender = models.CharField(max_length=128, verbose_name="发送/操作者username")
    receiver = models.CharField(max_length=128, verbose_name="接收者username")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")


class ProjectMessage(models.Model):
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    file_id = models.IntegerField(verbose_name="文件ID")
    username = models.CharField(max_length=128, verbose_name="操作者username")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")
