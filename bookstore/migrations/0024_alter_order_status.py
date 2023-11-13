# Generated by Django 4.2.7 on 2023-11-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0023_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('In Progress', 'In Progress'), ('Out of order', 'Out of order')], max_length=100),
        ),
    ]