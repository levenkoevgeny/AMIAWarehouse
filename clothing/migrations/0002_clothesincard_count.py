# Generated by Django 3.1.5 on 2022-02-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothesincard',
            name='count',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
    ]