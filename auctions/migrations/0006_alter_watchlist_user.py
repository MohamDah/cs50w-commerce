# Generated by Django 4.1.3 on 2022-12-03 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.CharField(max_length=64),
        ),
    ]
