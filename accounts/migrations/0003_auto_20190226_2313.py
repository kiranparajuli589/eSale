# Generated by Django 2.1.7 on 2019-02-26 17:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190226_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 28, 9, 776916, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 28, 9, 776916, tzinfo=utc), verbose_name='Registered Date'),
        ),
    ]
