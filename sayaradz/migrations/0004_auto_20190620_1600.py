# Generated by Django 2.1.7 on 2019-06-20 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0003_auto_20190401_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='distance',
            field=models.CharField(default=13000, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='year',
            field=models.CharField(default=2009, max_length=4),
            preserve_default=False,
        ),
    ]
