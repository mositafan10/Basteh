# Generated by Django 3.0.2 on 2020-02-20 13:27

import advertise.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertise', '0002_auto_20200218_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packet',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('0', 'تایید '), ('1', 'عدم تایید'), ('2', 'در انتظار پاسخ')], default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='packet',
            name='slug',
            field=models.CharField(db_index=True, default=advertise.models.generate_slug, editable=False, max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='packet',
            name='weight',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='travel',
            name='empty_weight',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)]),
        ),
    ]