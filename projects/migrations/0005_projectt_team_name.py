# Generated by Django 4.0.2 on 2022-08-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_filebin_projectbin_file_create_time_file_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectt',
            name='team_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
