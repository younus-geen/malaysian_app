# Generated by Django 4.2.4 on 2023-09-04 17:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malaysia_app', '0005_alter_zikr_count_zikr_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zikr_count',
            name='zikr_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 4, 17, 52, 2, 212677, tzinfo=datetime.timezone.utc)),
        ),
    ]