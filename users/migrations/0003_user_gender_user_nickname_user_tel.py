

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar_user_brief_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(default=0, max_length=3),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='user',
            name='tel',
            field=models.CharField(default='', max_length=18),
        ),
    ]
