# Generated by Django 3.1.2 on 2020-11-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_ericpro_cata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ericorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50)),
                ('accept', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=100, null=True)),
                ('shoplist', models.CharField(max_length=100, null=True)),
                ('shopqty', models.CharField(max_length=100, null=True)),
                ('cName', models.CharField(blank=True, default='', max_length=50)),
                ('cPhone', models.CharField(blank=True, default='', max_length=50)),
                ('cAddress', models.CharField(blank=True, default='', max_length=100)),
                ('cMail', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
