# Generated by Django 5.0.3 on 2024-04-15 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_user_delete_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owners',
            fields=[
                ('OwnerID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Users.user')),
                ('Username', models.CharField(max_length=255)),
                ('FirstName', models.CharField(blank=True, max_length=255, null=True)),
                ('MiddleName', models.CharField(blank=True, max_length=255, null=True)),
                ('LastName', models.CharField(max_length=255)),
                ('Password', models.CharField(max_length=255)),
                ('Email', models.EmailField(max_length=255)),
                ('ContactNumber1', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('ContactNumber2', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
            ],
        ),
    ]
