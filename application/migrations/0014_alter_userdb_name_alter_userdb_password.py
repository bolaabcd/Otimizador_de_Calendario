# Generated by Django 4.2.5 on 2023-10-08 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_alter_activitydb_value_alter_userdb_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='password',
            field=models.CharField(max_length=256),
        ),
    ]
