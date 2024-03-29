# Generated by Django 5.0.2 on 2024-03-19 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_message_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='homework',
            name='screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]
