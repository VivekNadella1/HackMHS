# Generated by Django 4.2.13 on 2024-05-18 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0005_alter_collegestats_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegestats',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='act',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='gpa',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='income',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='collegestats',
            name='sat',
            field=models.IntegerField(),
        ),
        migrations.AlterModelTable(
            name='collegestats',
            table=None,
        ),
    ]
