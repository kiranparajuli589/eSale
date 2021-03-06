# Generated by Django 3.0.2 on 2020-01-31 10:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='returntransaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='returntransaction',
            name='type',
            field=models.CharField(choices=[('SALE-RETURN', 'SALE-RETURN'), ('PURCHASE-RETURN', 'PURCHASE-RETURN')], default='SALE-RETURN', max_length=15),
        ),
        migrations.AlterField(
            model_name='salesreturn',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionstat',
            name='timestamp',
            field=models.DateField(default=datetime.date(2020, 1, 31)),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 31, 10, 41, 17, 328863, tzinfo=utc), verbose_name='Registered Date'),
        ),
    ]
