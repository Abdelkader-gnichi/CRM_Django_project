# Generated by Django 4.2.6 on 2023-11-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_remove_person_firstname_remove_person_lastname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='avatar',
            field=models.ImageField(blank=True, default='user_img.png', upload_to='profile_images'),
        ),
    ]
