# Generated by Django 4.2.5 on 2023-10-06 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_rename_loc_locationdb_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervaldb',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='intervaldb',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
