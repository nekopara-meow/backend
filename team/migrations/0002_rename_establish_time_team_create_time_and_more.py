# Generated by Django 4.0.2 on 2022-08-03 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='establish_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='establisher',
            new_name='creator',
        ),
    ]
