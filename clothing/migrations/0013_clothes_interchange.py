# Generated by Django 4.0.2 on 2022-03-14 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0012_remove_clothes_interchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='interchange',
            field=models.ManyToManyField(to='clothing.Clothes', verbose_name='Считается совместно с ...'),
        ),
    ]
