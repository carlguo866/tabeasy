# Generated by Django 3.2.14 on 2023-08-04 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0025_rename_spirit_team_spirit_score'),
        ('submission', '0023_auto_20230803_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spirit',
            name='id',
        ),
        migrations.AlterField(
            model_name='spirit',
            name='team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, primary_key=True, related_name='spirit', serialize=False, to='tourney.team'),
        ),
    ]
