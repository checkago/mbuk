# Generated by Django 3.2.9 on 2021-12-02 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_employee_work_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='work_start_date',
        ),
    ]