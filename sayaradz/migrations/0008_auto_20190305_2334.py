# Generated by Django 2.1.7 on 2019-03-05 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0007_auto_20190305_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='options',
            field=models.ManyToManyField(related_name='versions', to='sayaradz.Option'),
        ),
    ]