# Generated by Django 4.0.4 on 2022-06-22 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_tracking_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tracking_no',
        ),
    ]
