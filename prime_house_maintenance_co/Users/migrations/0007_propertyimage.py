# Generated by Django 5.0.3 on 2024-04-16 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_buys'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('Property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Users.property')),
            ],
        ),
    ]
