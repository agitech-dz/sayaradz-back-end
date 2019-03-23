# Generated by Django 2.1.7 on 2019-03-23 12:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import sayaradz.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minPrice', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('photo1', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path3)),
                ('photo2', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path3)),
                ('photo3', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path3)),
            ],
        ),
        migrations.CreateModel(
            name='Automobilist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('familyName', models.CharField(max_length=50)),
                ('password', models.CharField(default='', max_length=100)),
                ('address', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('avatar', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path4)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('numChassis', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('photo1', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path2)),
                ('photo2', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path2)),
                ('photo3', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path2)),
            ],
        ),
        migrations.CreateModel(
            name='CarSeller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('total', models.FloatField()),
                ('isVlidated', models.BooleanField(default=False)),
                ('automobilist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LigneTarif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateBegin', models.DateField()),
                ('dateEnd', models.DateField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, unique=True)),
                ('nationality', models.CharField(blank=True, max_length=45)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ManufacturerUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('avatar', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path1)),
                ('is_blocked', models.BooleanField(default=False)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Manufacturer')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Manufacturer')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('offredAmount', models.FloatField()),
                ('isAccepted', models.BooleanField(default=False)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Ad')),
                ('automobilist', models.ForeignKey(db_column='automobilist_id', on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel')),
                ('options', models.ManyToManyField(to='sayaradz.Option')),
            ],
        ),
        migrations.CreateModel(
            name='LigneTarifColor',
            fields=[
                ('lignetarif_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sayaradz.LigneTarif')),
            ],
            bases=('sayaradz.lignetarif',),
        ),
        migrations.CreateModel(
            name='LigneTarifOption',
            fields=[
                ('lignetarif_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sayaradz.LigneTarif')),
            ],
            bases=('sayaradz.lignetarif',),
        ),
        migrations.CreateModel(
            name='LigneTarifVersion',
            fields=[
                ('lignetarif_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sayaradz.LigneTarif')),
                ('code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Version')),
            ],
            bases=('sayaradz.lignetarif',),
        ),
        migrations.CreateModel(
            name='NewCar',
            fields=[
                ('car_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sayaradz.Car')),
            ],
            bases=('sayaradz.car',),
        ),
        migrations.CreateModel(
            name='OccCar',
            fields=[
                ('car_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sayaradz.Car')),
            ],
            bases=('sayaradz.car',),
        ),
        migrations.AddField(
            model_name='command',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Car'),
        ),
        migrations.AddField(
            model_name='color',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.MyModel'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(db_column='color', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sayaradz.Color'),
        ),
        migrations.AddField(
            model_name='car',
            name='options',
            field=models.ManyToManyField(to='sayaradz.Option'),
        ),
        migrations.AddField(
            model_name='car',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sayaradz.CarSeller'),
        ),
        migrations.AddField(
            model_name='car',
            name='version',
            field=models.ForeignKey(db_column='version', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sayaradz.Version'),
        ),
        migrations.AddField(
            model_name='automobilist',
            name='followedModels',
            field=models.ManyToManyField(to='sayaradz.MyModel'),
        ),
        migrations.AddField(
            model_name='automobilist',
            name='followedVersions',
            field=models.ManyToManyField(to='sayaradz.Version'),
        ),
        migrations.AddField(
            model_name='ad',
            name='automobilist',
            field=models.ForeignKey(db_column='owner_id', on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist'),
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together={('code', 'model')},
        ),
        migrations.AlterUniqueTogether(
            name='mymodel',
            unique_together={('code', 'manufacturer')},
        ),
        migrations.AddField(
            model_name='lignetarifoption',
            name='code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Option'),
        ),
        migrations.AddField(
            model_name='lignetarifcolor',
            name='code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Color'),
        ),
        migrations.AddField(
            model_name='ad',
            name='car',
            field=models.OneToOneField(db_column='car_numChassis', on_delete=django.db.models.deletion.CASCADE, to='sayaradz.OccCar'),
        ),
    ]
