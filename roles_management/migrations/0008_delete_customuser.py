# Generated by Django 5.1.4 on 2024-12-30 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles_management', '0007_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]