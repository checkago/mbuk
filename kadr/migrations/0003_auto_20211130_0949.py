# Generated by Django 3.2.9 on 2021-11-30 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0002_employeecard_branch_office'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Нименование')),
            ],
            options={
                'verbose_name': 'Статус сотрудника',
                'verbose_name_plural': 'Стаутсы сотрудников',
            },
        ),
        migrations.AddField(
            model_name='employeecard',
            name='children',
            field=models.IntegerField(blank=True, default=1, verbose_name='Несовершеннолетние дети'),
            preserve_default=False,
        ),
    ]