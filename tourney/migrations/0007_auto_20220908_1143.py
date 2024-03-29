# Generated by Django 3.2.14 on 2022-09-08 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0006_auto_20220907_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='pairing',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pairings', related_query_name='pairing', to='tourney.tournament'),
        ),
        migrations.AlterField(
            model_name='pairing',
            name='division',
            field=models.CharField(blank=True, choices=[('Disney', 'Disney'), ('Universal', 'Universal')], max_length=100, null=True),
        ),
    ]
