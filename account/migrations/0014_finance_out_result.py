# Generated by Django 4.2 on 2023-04-28 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_invoice_invoice_date_payment_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='finance_out',
            name='result',
            field=models.IntegerField(default=0),
        ),
    ]