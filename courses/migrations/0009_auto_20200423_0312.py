# Generated by Django 3.0.5 on 2020-04-23 02:12

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20200423_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='thumbnail',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='thumbnail'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='video'),
        ),
    ]
