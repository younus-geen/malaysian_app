# Generated by Django 4.2.4 on 2023-08-24 21:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('malaysia_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='zikr_count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zikr_count', models.IntegerField()),
                ('zikr_date', models.DateTimeField(default=datetime.datetime(2023, 8, 24, 21, 43, 45, 860943, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
