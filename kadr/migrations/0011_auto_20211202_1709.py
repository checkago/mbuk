# Generated by Django 3.2.9 on 2021-12-02 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0010_alter_employeestatus_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecard',
            name='bib_experience_before',
            field=models.IntegerField(blank=True, null=True, verbose_name='Предыдущий стаж библиотечный'),
        ),
        migrations.AlterField(
            model_name='employeecard',
            name='experience_before',
            field=models.IntegerField(verbose_name='Предыдущий стаж полный'),
        ),
    ]
