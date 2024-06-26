# Generated by Django 5.0.3 on 2024-04-15 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=50)),
                ('PropertyID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.property')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.user')),
            ],
            options={
                'unique_together': {('UserID', 'PropertyID')},
            },
        ),
    ]
