# Generated by Django 2.1.7 on 2019-03-23 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0019_auto_20190323_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='description',
            field=models.TextField(default='text'),
            preserve_default=False,
        ),
    ]