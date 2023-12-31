# Generated by Django 4.2.5 on 2023-11-23 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_bookingworker_payment_receipt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingworker',
            name='payment_receipt',
        ),
        migrations.RemoveField(
            model_name='bookingworker',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='bookingworker',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_receipt', models.FileField(blank=True, null=True, upload_to='payment_receipts/')),
                ('razorpay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='home.bookingworker')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
