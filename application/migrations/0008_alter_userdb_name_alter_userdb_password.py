# Generated by Django 4.2.5 on 2023-10-07 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_alter_activitydb_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdb',
            name='name',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='userdb',
            name='password',
            field=models.CharField(max_length=1000),
        ),
    ]
