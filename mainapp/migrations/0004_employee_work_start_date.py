# Generated by Django 3.2.9 on 2021-12-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211126_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='work_start_date',
            field=models.DateField(null=True, verbose_name='Дата приема на работу'),
        ),
    ]
