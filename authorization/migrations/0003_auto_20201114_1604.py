# Generated by Django 2.2.2 on 2020-11-14 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_auto_20201113_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(db_index=True, max_length=256),
        ),
    ]
