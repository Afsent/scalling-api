# Generated by Django 3.1.2 on 2020-10-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resize_api', '0006_auto_20201017_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.BinaryField(blank=True),
        ),
    ]
