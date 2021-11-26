# Generated by Django 3.2.9 on 2021-11-23 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211123_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='primary',
            field=models.BooleanField(default=False, verbose_name='Основная'),
        ),
        migrations.AlterField(
            model_name='department',
            name='parent_branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.branchoffice', verbose_name='Входит в состав'),
        ),
    ]
