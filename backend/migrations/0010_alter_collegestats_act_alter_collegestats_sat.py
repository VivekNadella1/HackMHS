# Generated by Django 4.2.13 on 2024-05-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_collegestats_gpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegestats',
            name='act',
            field=models.IntegerField(default=32),
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='sat',
            field=models.IntegerField(default=1400),
        ),
    ]