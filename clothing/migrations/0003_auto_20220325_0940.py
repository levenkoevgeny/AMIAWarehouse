# Generated by Django 2.2.7 on 2022-03-25 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothing', '0002_auto_20220323_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='descriptionitem',
            options={'ordering': ('id',), 'verbose_name': 'Описание движения в карточке', 'verbose_name_plural': 'Описания движений в карточке'},
        ),
        migrations.AlterModelOptions(
            name='normitemsinnorm',
            options={'ordering': ('id',), 'verbose_name': 'Наименование в норме', 'verbose_name_plural': 'Наименования в норме'},
        ),
        migrations.AddField(
            model_name='movement',
            name='replacing_what',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clothing.Movement'),
        ),
        migrations.AlterField(
            model_name='normitem',
            name='item_clothes',
            field=models.ManyToManyField(to='clothing.Clothes', verbose_name='Совокупность вещей'),
        ),
        migrations.AlterUniqueTogether(
            name='normitemsinnorm',
            unique_together={('norm', 'norm_item')},
        ),
    ]
