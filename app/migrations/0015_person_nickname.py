# Generated by Django 3.2.5 on 2021-07-24 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='nick', max_length=50),
        ),
    ]
