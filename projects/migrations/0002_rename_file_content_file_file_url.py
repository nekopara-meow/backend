# Generated by Django 4.0.2 on 2022-08-05 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='file_content',
            new_name='file_url',
        ),
    ]
