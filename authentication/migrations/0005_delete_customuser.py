# Generated by Django 5.1.3 on 2024-11-24 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_kicd_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]