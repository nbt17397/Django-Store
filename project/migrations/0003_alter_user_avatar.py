# Generated by Django 4.0.5 on 2022-08-01 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, upload_to='staticfiles/static/uploads/%Y/%m'),
        ),
    ]
