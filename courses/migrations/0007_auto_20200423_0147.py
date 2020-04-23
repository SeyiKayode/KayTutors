# Generated by Django 3.0.5 on 2020-04-23 00:47

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200415_0108'),
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