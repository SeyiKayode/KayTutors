# Generated by Django 3.0.5 on 2020-04-23 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20200423_0312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(upload_to=''),
        ),
    ]
