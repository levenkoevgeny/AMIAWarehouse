# Generated by Django 2.2.7 on 2022-03-31 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0005_auto_20220329_1238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='decree_finish',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='decree_start',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_on_decree',
        ),
    ]