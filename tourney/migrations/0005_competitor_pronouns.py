# Generated by Django 3.2.14 on 2022-09-08 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0004_tournament_individual_award_rank_plus_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='pronouns',
            field=models.CharField(blank=True, choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], max_length=20, null=True),
        ),
    ]
