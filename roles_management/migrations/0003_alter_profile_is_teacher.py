# Generated by Django 5.1.4 on 2024-12-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles_management', '0002_profile_is_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]