# Generated by Django 4.1.4 on 2022-12-20 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_userinfo_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='cus_type',
        ),
    ]
