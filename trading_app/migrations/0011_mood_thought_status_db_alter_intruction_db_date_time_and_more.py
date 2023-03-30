# Generated by Django 4.1.4 on 2023-03-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_app', '0010_intruction_db_trading_plans'),
    ]

    operations = [
        migrations.CreateModel(
            name='mood_thought_status_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mood', models.CharField(max_length=100, null=True)),
                ('Market_condition', models.CharField(max_length=100, null=True)),
                ('Preparation', models.CharField(max_length=100, null=True)),
                ('Thought', models.CharField(max_length=100, null=True)),
                ('date_time', models.DateTimeField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='intruction_db',
            name='date_time',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order_db',
            name='PE_VOLM',
            field=models.DateTimeField(max_length=100, null=True),
        ),
    ]
