# Generated by Django 2.2.2 on 2019-07-09 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_session_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='high_score',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]
