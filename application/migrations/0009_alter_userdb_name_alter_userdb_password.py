# Generated by Django 4.2.5 on 2023-10-07 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_alter_userdb_name_alter_userdb_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
