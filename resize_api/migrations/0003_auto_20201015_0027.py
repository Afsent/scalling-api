# Generated by Django 3.1.2 on 2020-10-14 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resize_api', '0002_auto_20201014_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='pics'),
        ),
    ]
