# Generated by Django 4.2.13 on 2024-05-18 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_collegestats_gpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegestats',
            name='act',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='sat',
            field=models.FloatField(),
        ),
    ]