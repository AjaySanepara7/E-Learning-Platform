# Generated by Django 5.1.4 on 2024-12-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_teacher',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]