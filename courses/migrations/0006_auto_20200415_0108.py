# Generated by Django 2.2.7 on 2020-04-15 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20200415_0103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='video_url',
            new_name='video',
        ),
    ]
