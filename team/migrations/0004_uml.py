# Generated by Django 4.0.2 on 2022-08-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_alter_team_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uml',
            fields=[
                ('creator', models.CharField(max_length=128)),
                ('uml_id', models.AutoField(primary_key=True, serialize=False)),
                ('uml_url', models.CharField(max_length=1024)),
            ],
        ),
    ]