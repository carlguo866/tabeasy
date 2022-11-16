# Generated by Django 3.2.14 on 2022-11-16 05:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0016_auto_20221108_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='school',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(default='Team', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='case',
            field=models.URLField(blank=True, help_text='Case Link:', null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='division_team_num',
            field=models.IntegerField(default=10, help_text='How many teams do you have?'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='hide_comments',
            field=models.BooleanField(default=False, help_text='Is the tournament in-person?'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='individual_award_rank_plus_record',
            field=models.BooleanField(default=False, help_text="Do you include the team's record when calculating individual awards?"),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='judges',
            field=models.IntegerField(default=2, help_text='How many judges do you count into the result?'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(help_text='Tournament Name:', max_length=40),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='p_choice',
            field=models.CharField(choices=[('Prosecution', 'Criminal'), ('Plaintiff', 'Civil')], help_text='Is your case a Civil or Criminal case', max_length=40),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='presiding_judge_script',
            field=models.URLField(blank=True, help_text='Presiding Judge Script (leave blank if not applicable):', null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='publish_ballot_scores',
            field=models.BooleanField(default=False, help_text='Do you want to publish scores ballot or just the comments?'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='rank_nums',
            field=models.IntegerField(default=5, help_text='How many competitors (attorneys/witnesses) do judges rank?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='roe',
            field=models.URLField(blank=True, help_text='Rules of Evidence Link:', null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='wit_nums',
            field=models.IntegerField(default=3, help_text='How many witnesses does each side call?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='zoom_link',
            field=models.URLField(blank=True, help_text='Zoom Meeting Link (leave blank if not applicable):', null=True),
        ),
    ]
