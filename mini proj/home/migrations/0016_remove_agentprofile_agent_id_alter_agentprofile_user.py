# Generated by Django 4.2.5 on 2023-11-18 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_agentprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentprofile',
            name='agent_id',
        ),
        migrations.AlterField(
            model_name='agentprofile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
