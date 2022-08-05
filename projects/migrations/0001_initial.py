# Generated by Django 4.0.2 on 2022-08-05 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('project_id', models.IntegerField(verbose_name='文件所属项目ID')),
                ('file_name', models.CharField(max_length=128)),
                ('file_type', models.IntegerField(verbose_name='文件种类')),
                ('creator', models.CharField(max_length=128)),
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_content', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Projectt',
            fields=[
                ('team_id', models.IntegerField(verbose_name='项目所属团队ID')),
                ('project_id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目ID')),
                ('project_name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('creator', models.CharField(max_length=128, verbose_name='创始人用户名')),
                ('create_time', models.DateTimeField(auto_now_add=True, max_length=80, verbose_name='项目成立时间')),
                ('brief_intro', models.CharField(default='我不到啊', max_length=1024)),
            ],
        ),
    ]
