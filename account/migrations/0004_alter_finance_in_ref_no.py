# Generated by Django 4.2 on 2023-06-17 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_finance_in_ref_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finance_in',
            name='ref_no',
            field=models.CharField(default=0, max_length=64, unique=True),
        ),
    ]