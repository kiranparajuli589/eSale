# Generated by Django 2.1.7 on 2019-02-26 17:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20190226_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 40, 58, 422302, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 40, 58, 422302, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Order'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 40, 58, 422302, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 26, 17, 40, 58, 422302, tzinfo=utc), verbose_name='Registered Date'),
        ),
    ]
