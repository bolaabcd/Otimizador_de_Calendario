# Generated by Django 4.2.5 on 2023-10-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0014_alter_userdb_name_alter_userdb_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
