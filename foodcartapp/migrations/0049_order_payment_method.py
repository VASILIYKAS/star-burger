# Generated by Django 3.2.15 on 2025-06-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20250605_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличными'), ('card', 'Картой онлайн'), ('card_courier', 'Картой курьеру')], db_index=True, default='card', max_length=20, verbose_name='Способ оплаты'),
        ),
    ]
