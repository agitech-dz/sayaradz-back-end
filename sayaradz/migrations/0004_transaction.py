# Generated by Django 2.2.3 on 2019-09-13 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0003_auto_20190913_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(max_length=25)),
                ('amount', models.FloatField()),
                ('automobilist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
                ('command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Command')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('id', 'automobilist', 'command')},
            },
        ),
    ]
