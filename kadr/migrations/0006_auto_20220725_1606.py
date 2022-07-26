# Generated by Django 3.2.9 on 2022-07-25 13:06

from django.db import migrations, models
import utils.uploading


class Migration(migrations.Migration):

    dependencies = [
        ('kadr', '0005_auto_20220725_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeecard',
            name='inn',
            field=models.CharField(blank=True, max_length=10, verbose_name='ИНН'),
        ),
        migrations.AddField(
            model_name='employeecard',
            name='passport_copy',
            field=models.FileField(blank=True, upload_to=utils.uploading.file_upload_function, verbose_name='Копия паспорта'),
        ),
        migrations.AddField(
            model_name='employeecard',
            name='snils',
            field=models.CharField(blank=True, max_length=11, verbose_name='СНИЛС'),
        ),
    ]