# Generated by Django 2.1.5 on 2022-03-26 19:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20220326_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='title',
            field=models.CharField(default='hi', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='place_type',
            field=models.CharField(choices=[('Restaurant', 'Restaurant'), ('Cafe', 'Cafe'), ('Fast Food', 'Fast Food'), ('Nightlife', 'Nightlife'), ('Anywhere', 'Anywhere')], max_length=128),
        ),
    ]
