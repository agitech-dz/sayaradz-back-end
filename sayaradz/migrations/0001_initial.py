# Generated by Django 2.1.7 on 2019-02-27 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sayaradz.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', sayaradz.models.UserManager()),
            ],
        ),
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
                ('price', models.FloatField()),
                ('isVlidated', models.BooleanField(default=False)),
                ('automobilist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Automobilist')),
            ],
        ),
        migrations.CreateModel(
            name='LigneTarif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataBegin', models.DateField(auto_now=True)),
                ('dataEnd', models.DateField(auto_now=True)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MakeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('avatar', models.ImageField(blank=True, upload_to=sayaradz.models.get_upload_path1)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Make')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Make')),
            ],
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
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Model')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
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
            model_name='option',
            name='versions',
            field=models.ManyToManyField(to='sayaradz.Version'),
        ),
        migrations.AddField(
            model_name='command',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Car'),
        ),
        migrations.AddField(
            model_name='color',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sayaradz.Model'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(db_column='color', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sayaradz.Model'),
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
            field=models.ForeignKey(db_column='version', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sayaradz.Make'),
        ),
        migrations.AddField(
            model_name='automobilist',
            name='followedModels',
            field=models.ManyToManyField(to='sayaradz.Model'),
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
