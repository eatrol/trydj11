# Generated by Django 3.1.2 on 2020-11-30 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20201126_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='ericpro',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='ericpro',
            name='isnew',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ericpro',
            name='isprice',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ericpro',
            name='subcata',
            field=models.CharField(default='aa', max_length=20),
            preserve_default=False,
        ),
    ]