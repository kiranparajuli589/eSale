# Generated by Django 3.0.3 on 2020-02-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]
