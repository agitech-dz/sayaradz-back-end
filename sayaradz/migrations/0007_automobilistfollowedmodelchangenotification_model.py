# Generated by Django 2.2.3 on 2019-09-14 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0006_auto_20190913_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='automobilistfollowedmodelchangenotification',
            name='model',
            field=models.ForeignKey(default='m1', on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel'),
            preserve_default=False,
        ),
    ]
