# Generated by Django 5.0.3 on 2024-04-20 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0026_remove_services_employees'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.employee')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.services')),
            ],
        ),
    ]