# Generated by Django 4.1 on 2022-08-10 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_file_name_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="height",
            field=models.IntegerField(null=True, verbose_name="原型设计高度"),
        ),
        migrations.AddField(
            model_name="file",
            name="width",
            field=models.IntegerField(null=True, verbose_name="原型设计长度"),
        ),
    ]