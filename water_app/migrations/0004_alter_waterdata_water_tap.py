# Generated by Django 4.2.5 on 2023-11-15 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_app', '0003_alter_waterdata_water_tap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterdata',
            name='water_tap',
            field=models.CharField(max_length=20),
        ),
    ]
