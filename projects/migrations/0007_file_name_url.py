# Generated by Django 4.0.2 on 2022-08-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_file_projects_fi_project_bdb067_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name_url',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
