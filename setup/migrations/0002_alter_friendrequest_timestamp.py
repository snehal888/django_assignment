# Generated by Django 5.1.1 on 2024-09-05 13:26

import setup.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='timestamp',
            field=models.CharField(max_length=230, null=True, validators=[setup.validations.is_valid_timestamp]),
        ),
    ]
