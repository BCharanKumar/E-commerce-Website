# Generated by Django 5.0.7 on 2025-01-06 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_orderaddress_address_line_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderaddress',
            name='email',
            field=models.EmailField(default='customer@gmail.com', max_length=254, unique=True),
        ),
    ]
