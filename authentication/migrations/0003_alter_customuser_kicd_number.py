# Generated by Django 5.1.3 on 2024-11-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser_kicd_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='kicd_number',
            field=models.CharField(blank=True, help_text="User's KICD number", max_length=50),
        ),
    ]