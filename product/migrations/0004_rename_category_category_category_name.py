# Generated by Django 4.0.4 on 2022-06-14 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_options_remove_category_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='category_name',
        ),
    ]
