# Generated by Django 2.0.2 on 2018-04-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_order_orderitem_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ship_address2',
            field=models.TextField(blank=True, null=True),
        ),
    ]
