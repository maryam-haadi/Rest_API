# Generated by Django 4.2.4 on 2023-08-27 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_transaction_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='account',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.account'),
        ),
    ]
