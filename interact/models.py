from django.db import models
# Create your models here.
from django.db import models
import datetime


# Create your models here.


class Member_in_Team(models.Model):
    username = models.CharField(max_length=128)
    team_id = models.IntegerField(verbose_name="团队ID")
    priority = models.IntegerField(verbose_name="该成员在该项目中权限等级")



class PersonalMessage(models.Model):
    sender = models.CharField(max_length=128, verbose_name="发送/操作者username")
    receiver = models.CharField(max_length=128, verbose_name="接收者username")
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")
    message_id = models.AutoField(primary_key=True)
# 被踢出团队，被邀请加入团队，被设为管理，被取消管理


class TeamMessage(models.Model):
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    sender = models.CharField(max_length=128, verbose_name="发送/操作者username")
    receiver = models.CharField(max_length=128, verbose_name="接收者username")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")
    message_id = models.AutoField(primary_key=True)
# x邀请y加入团队，x把y踢出团队，x把y设为管理，x撤销y的管理，x新建项目，x删除项目


class ProjectMessage(models.Model):
    team_id = models.IntegerField(verbose_name="团队ID")
    project_id = models.IntegerField(verbose_name="项目ID")
    file_id = models.IntegerField(verbose_name="文件ID")
    username = models.CharField(max_length=128, verbose_name="操作者username")
    send_time = models.DateTimeField(max_length=80, verbose_name="消息发送时间", auto_now_add=True)
    message_type = models.IntegerField(verbose_name="信息种类")
    message_id = models.AutoField(primary_key=True)
# x新建了文件y，x删除了文件y，x开放文件y的预览，x关闭文件y的预览
