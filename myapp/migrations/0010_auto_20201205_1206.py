# Generated by Django 3.1.2 on 2020-12-05 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20201205_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ericpro',
            name='image1',
            field=models.ImageField(upload_to='logo'),
        ),
    ]
