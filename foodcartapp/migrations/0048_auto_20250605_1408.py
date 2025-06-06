# Generated by Django 3.2.15 on 2025-06-05 09:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='assembly_started_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата начала сборки'),
        ),
        migrations.AddField(
            model_name='order',
            name='completed_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_started_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата начала доставки'),
        ),
    ]
