# Generated by Django 4.2.6 on 2023-11-02 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0009_alter_person_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='avatar',
            field=models.ImageField(blank=True, default='user_img.png', upload_to='profile_images'),
        ),
    ]
