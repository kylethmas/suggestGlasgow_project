# Generated by Django 2.2.26 on 2022-03-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20220325_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='place_image',
            field=models.ImageField(blank=True, default='/place_images/Default.jpg', upload_to='place_images'),
        ),
    ]
