# Generated by Django 4.2.6 on 2023-11-05 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_migratoryworker_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='migratoryworker',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
