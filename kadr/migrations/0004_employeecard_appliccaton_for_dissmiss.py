# Generated by Django 3.2.9 on 2022-07-23 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0003_auto_20220723_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecard',
            name='appliccaton_for_dissmiss',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kadr.applicationfordismissal', verbose_name='Заявление на увольнение'),
        ),
    ]