# Generated by Django 2.2.3 on 2019-09-13 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0005_automobilistpostoffernotification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automobilistnotification',
            name='notification_type',
            field=models.CharField(choices=[('OA', 'offer_accepted'), ('MC', 'model_changed'), ('VC', 'version_changed'), ('CV', 'command_valitaded'), ('OP', 'offer_posted')], default='OA', max_length=3),
        ),
    ]