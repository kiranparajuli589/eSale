# Generated by Django 2.1.7 on 2019-05-19 07:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20190510_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 19, 7, 44, 57, 623933, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 19, 7, 44, 57, 623933, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionstat',
            name='timestamp',
            field=models.DateField(default=datetime.date(2019, 5, 19)),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 19, 7, 44, 57, 623933, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Email Address'),
        ),
    ]
