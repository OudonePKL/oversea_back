# Generated by Django 5.0.2 on 2024-02-21 06:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_order_total_prices_orderitem_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="post_office",
        ),
    ]