# Generated by Django 4.2.4 on 2023-09-10 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malaysia_app', '0016_target_count_alter_zikr_count_zikr_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='target_count',
            old_name='traget_count',
            new_name='target_count',
        ),
        migrations.AlterField(
            model_name='zikr_count',
            name='zikr_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 13, 45, 11, 481455, tzinfo=datetime.timezone.utc)),
        ),
    ]