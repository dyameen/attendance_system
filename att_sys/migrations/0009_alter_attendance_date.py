# Generated by Django 3.2.15 on 2022-09-20 08:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('att_sys', '0008_alter_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]