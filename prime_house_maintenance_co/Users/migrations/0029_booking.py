# Generated by Django 5.0.3 on 2024-04-20 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0028_delete_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('BookingID', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('Status', models.BooleanField()),
                ('EmployeeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.employee')),
                ('PropertyID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.property')),
                ('ServiceID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.services')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.user')),
            ],
        ),
    ]
