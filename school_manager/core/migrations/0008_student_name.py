# Generated by Django 5.0.2 on 2024-03-11 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
