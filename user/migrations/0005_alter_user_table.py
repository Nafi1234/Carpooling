# Generated by Django 4.2.6 on 2023-10-05 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_is_superadmin_user_is_superuser_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
