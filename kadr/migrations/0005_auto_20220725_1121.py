# Generated by Django 3.2.9 on 2022-07-25 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0004_employeecard_appliccaton_for_dissmiss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeecard',
            name='status',
        ),
        migrations.DeleteModel(
            name='EmployeeStatus',
        ),
    ]
