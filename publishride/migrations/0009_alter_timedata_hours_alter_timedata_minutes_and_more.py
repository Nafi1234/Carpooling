# Generated by Django 4.2.6 on 2023-11-23 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishride', '0008_alter_payment_order_id_alter_payment_payment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timedata',
            name='hours',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='timedata',
            name='minutes',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='timedata',
            name='period',
            field=models.CharField(max_length=5),
        ),
    ]
