# Generated by Django 5.0.2 on 2024-03-12 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_teacher_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
    ]
