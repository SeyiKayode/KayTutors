# Generated by Django 3.0.5 on 2020-04-24 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]