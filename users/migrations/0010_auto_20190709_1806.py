# Generated by Django 2.2.2 on 2019-07-09 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190709_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='high_bonus_level',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='high_score_level',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]
