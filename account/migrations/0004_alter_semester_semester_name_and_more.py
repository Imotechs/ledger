# Generated by Django 4.1.7 on 2023-05-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_record_reg_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_name',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_name',
            field=models.CharField(max_length=15),
        ),
    ]
