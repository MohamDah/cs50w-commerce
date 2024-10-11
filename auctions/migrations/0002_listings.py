# Generated by Django 4.1.3 on 2022-11-29 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=300)),
                ('bid', models.IntegerField()),
                ('image', models.URLField()),
                ('category', models.CharField(max_length=64)),
            ],
        ),
    ]
