# Generated by Django 3.0.6 on 2020-12-13 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantratingapi', '0004_auto_20201213_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addeddishrating',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='addedrating',
            name='restaurant',
        ),
    ]
