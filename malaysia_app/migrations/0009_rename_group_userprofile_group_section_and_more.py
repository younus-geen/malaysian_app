# Generated by Django 4.2.4 on 2023-09-04 18:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malaysia_app', '0008_rename_group_section_userprofile_group_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='group',
            new_name='group_section',
        ),
        migrations.AlterField(
            model_name='zikr_count',
            name='zikr_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 4, 18, 54, 48, 948687, tzinfo=datetime.timezone.utc)),
        ),
    ]
