# Generated by Django 2.1.7 on 2019-03-04 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Model',
            new_name='MyModel',
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='manufactureruser',
            options={'ordering': ['id']},
        ),
    ]
