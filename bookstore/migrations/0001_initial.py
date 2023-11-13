# Generated by Django 4.2.6 on 2023-10-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('phone', models.IntegerField(max_length=12)),
                ('addres', models.TextField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
