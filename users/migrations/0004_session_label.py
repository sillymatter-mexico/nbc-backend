# Generated by Django 2.2.2 on 2019-07-01 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('users', '0003_clientuser_passwordtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Label'),
        ),
    ]
