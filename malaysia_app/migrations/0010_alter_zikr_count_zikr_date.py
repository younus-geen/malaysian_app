# Generated by Django 4.2.4 on 2023-09-04 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malaysia_app', '0009_rename_group_userprofile_group_section_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zikr_count',
            name='zikr_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 4, 18, 55, 3, 918143, tzinfo=datetime.timezone.utc)),
        ),
    ]
