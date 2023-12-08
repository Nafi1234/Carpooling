# Generated by Django 4.2.6 on 2023-11-15 08:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('publishride', '0006_reuquestride_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='Order ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default=2.0, max_length=200, verbose_name='Payment ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='signature',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Signature'),
        ),
    ]