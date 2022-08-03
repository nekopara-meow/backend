from django.db import models
# Create your models here.
from django.db import models
import datetime
# Create your models here.


class Member_in_Team(models.Model):
    username = models.CharField(max_length=128)
    team_id = models.IntegerField(verbose_name="团队ID")
    priority = models.IntegerField(verbose_name="该成员在该项目中权限等级")
