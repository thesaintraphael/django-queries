# Generated by Django 3.2.5 on 2021-07-24 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_bloodbank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodbank',
            name='existent_amount',
        ),
    ]
