# Generated by Django 4.2.13 on 2024-05-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_rename_course_name_apcourse_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegestats',
            name='act',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
