# Generated by Django 4.1.3 on 2022-12-01 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_seller_alter_listings_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='seller',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
