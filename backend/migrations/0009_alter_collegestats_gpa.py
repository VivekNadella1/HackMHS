# Generated by Django 4.2.13 on 2024-05-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_extracurricularactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegestats',
            name='gpa',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
    ]