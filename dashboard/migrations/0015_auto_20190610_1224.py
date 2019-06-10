# Generated by Django 2.1.7 on 2019-06-10 06:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20190608_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 6, 39, 5, 831734, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tot_due',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tot_recved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='purchasereturn',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 6, 39, 5, 831734, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='salesreturn',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 6, 39, 5, 831734, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 6, 39, 5, 831734, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transactionstat',
            name='timestamp',
            field=models.DateField(default=datetime.date(2019, 6, 10)),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 10, 6, 39, 5, 831734, tzinfo=utc), verbose_name='Registered Date'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='tot_due',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='tot_recved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
