# Generated by Django 4.1.4 on 2023-02-22 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0004_order_db_ce_oi'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_db',
            name='CE_IV',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_db',
            name='PE_IV',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_db',
            name='PE_OI',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
