# Generated by Django 4.0.2 on 2022-08-09 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_projectt_team_name'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='file',
            index=models.Index(fields=['project_id'], name='projects_fi_project_bdb067_idx'),
        ),
        migrations.AddIndex(
            model_name='file',
            index=models.Index(fields=['project_id', 'creator'], name='projects_fi_project_d6c949_idx'),
        ),
        migrations.AddIndex(
            model_name='file',
            index=models.Index(fields=['project_id', 'file_type'], name='projects_fi_project_bc85d7_idx'),
        ),
        migrations.AddIndex(
            model_name='projectt',
            index=models.Index(fields=['team_id'], name='projects_pr_team_id_5bc48b_idx'),
        ),
    ]