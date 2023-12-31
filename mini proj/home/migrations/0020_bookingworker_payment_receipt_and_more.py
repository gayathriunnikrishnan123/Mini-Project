# Generated by Django 4.2.5 on 2023-11-22 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingworker',
            name='payment_receipt',
            field=models.FileField(blank=True, null=True, upload_to='payment_receipts/'),
        ),
        migrations.AddField(
            model_name='bookingworker',
            name='payment_status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
