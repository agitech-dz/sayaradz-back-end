# Generated by Django 2.1.7 on 2019-03-06 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0011_remove_version_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Manufacturer'),
            preserve_default=False,
        ),
    ]
