# Generated by Django 4.2.5 on 2023-11-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_migratoryworker_passport_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='migratoryworker',
            name='work_permit',
            field=models.TextField(blank=True, null=True),
        ),
    ]
