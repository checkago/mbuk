# Generated by Django 3.2.9 on 2022-06-17 09:36

from django.db import migrations, models
import django.db.models.deletion
import utils.uploading


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0011_auto_20211202_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeecard',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=utils.uploading.image_upload_function, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='employeecard',
            name='place_of_stay_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_place_of_stay_address', to='kadr.employeeaddress', verbose_name='Фактический адрес проживания'),
        ),
    ]
