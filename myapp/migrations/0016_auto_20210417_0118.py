# Generated by Django 3.1.2 on 2021-04-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20201205_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='ericuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=50)),
                ('userid', models.CharField(blank=True, default='', max_length=50)),
                ('password', models.CharField(blank=True, default='', max_length=50)),
                ('score', models.DecimalField(decimal_places=2, max_digits=7)),
                ('data', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='description',
            field=models.CharField(default='this is my first website', max_length=500),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='image',
            field=models.CharField(blank=True, default='img/product-8.png', max_length=50),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='image1',
            field=models.ImageField(blank=True, default='eee', upload_to='pphoto'),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='image2',
            field=models.ImageField(blank=True, default='bb', upload_to='pphoto'),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='image3',
            field=models.ImageField(blank=True, default='c', upload_to='pphoto'),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='isnew',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='isprice',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ericpro',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=7),
        ),
    ]