# Generated by Django 5.0.3 on 2024-04-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0017_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='img/'),
        ),
    ]
