# Generated by Django 2.1.7 on 2019-03-06 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0009_auto_20190306_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Manufacturer'),
            preserve_default=False,
        ),
    ]