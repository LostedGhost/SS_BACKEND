# Generated by Django 5.1 on 2024-09-22 18:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_authuser_date_expiration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 19, 52, 25, 987227)),
        ),
        migrations.AlterField(
            model_name='membremaison',
            name='date_ajout',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 22, 19, 37, 25, 987227)),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='date_ajout',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
