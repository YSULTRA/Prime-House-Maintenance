# Generated by Django 5.0.3 on 2024-04-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0024_remove_booking_empid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='EmpID',
        ),
        migrations.AddField(
            model_name='services',
            name='Employees',
            field=models.ManyToManyField(to='Users.employee'),
        ),
    ]
