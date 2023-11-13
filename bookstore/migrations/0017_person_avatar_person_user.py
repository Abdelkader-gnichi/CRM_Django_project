# Generated by Django 4.2.6 on 2023-11-02 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0016_remove_person_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='avatar',
            field=models.ImageField(blank=True, default='user_img.png', null=True, upload_to='profile_images'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]