# Generated by Django 4.0.2 on 2022-03-13 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0008_alter_clothes_options_employee_enlisted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='has_to_be_deposited',
            field=models.BooleanField(default=False, verbose_name='Подлежит сдаче'),
        ),
    ]
