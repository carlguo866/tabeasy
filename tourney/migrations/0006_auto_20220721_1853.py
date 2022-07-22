# Generated by Django 3.2.14 on 2022-07-22 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0005_auto_20220721_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pairing',
            name='rounds',
        ),
        migrations.AddField(
            model_name='round',
            name='pairing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rounds', related_query_name='round', to='tourney.pairing'),
        ),
    ]