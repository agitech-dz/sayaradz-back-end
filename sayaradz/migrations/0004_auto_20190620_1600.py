# Generated by Django 2.1.7 on 2019-06-20 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayaradz', '0003_auto_20190401_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowedModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='FollowedVersions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
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
            field=models.CharField(default=13000, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='year',
            field=models.CharField(default=2009, max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='followedversions',
            name='automobilist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist'),
        ),
        migrations.AddField(
            model_name='followedversions',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Version'),
        ),
        migrations.AddField(
            model_name='followedmodels',
            name='automobilist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist'),
        ),
        migrations.AddField(
            model_name='followedmodels',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel'),
        ),
    ]