# Generated by Django 3.0 on 2021-04-16 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='website',
            field=models.URLField(default='ajul.github.io'),
        ),
    ]
