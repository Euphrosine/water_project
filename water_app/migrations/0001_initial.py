# Generated by Django 4.2.5 on 2023-11-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WaterData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('status_type', models.CharField(max_length=100)),
                ('quality', models.CharField(max_length=100)),
            ],
        ),
    ]
