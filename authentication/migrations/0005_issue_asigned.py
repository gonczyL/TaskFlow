# Generated by Django 5.1.4 on 2025-01-07 13:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_customuser_team_alter_issue_logged_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='asigned',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
