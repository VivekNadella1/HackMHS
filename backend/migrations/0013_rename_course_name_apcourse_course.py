# Generated by Django 4.2.13 on 2024-05-18 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_apcourse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apcourse',
            old_name='course_name',
            new_name='course',
        ),
    ]