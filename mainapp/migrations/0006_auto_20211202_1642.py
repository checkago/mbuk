# Generated by Django 3.2.9 on 2021-12-02 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_remove_employee_work_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='whatsapp',
        ),
    ]