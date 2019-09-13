# Generated by Django 2.2.3 on 2019-07-30 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0005_auto_20190624_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='automobilist',
            name='followedModels',
        ),
        migrations.RemoveField(
            model_name='automobilist',
            name='followedVersions',
        ),
        migrations.AddField(
            model_name='ad',
            name='distance',
            field=models.CharField(default=1200, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='year',
            field=models.CharField(default=2001, max_length=4),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FollowedVersions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('automobilist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Version')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='FollowedModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('automobilist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]