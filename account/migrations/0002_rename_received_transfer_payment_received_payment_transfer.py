# Generated by Django 4.2 on 2023-05-17 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='received_transfer',
            new_name='received_payment_transfer',
        ),
    ]