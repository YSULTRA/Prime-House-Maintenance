# Generated by Django 5.0.3 on 2024-04-20 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_booking_empid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='EmpID',
        ),
    ]
