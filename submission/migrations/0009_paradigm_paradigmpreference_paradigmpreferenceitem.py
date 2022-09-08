# Generated by Django 3.2.14 on 2022-09-08 05:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0006_auto_20220907_2215'),
        ('submission', '0008_remove_character_pronouns'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paradigm',
            fields=[
                ('judge', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='paradigm', serialize=False, to='tourney.judge')),
                ('experience_years', models.DecimalField(decimal_places=1, default=1, help_text='How many years of mock trial experience do you have?', max_digits=3)),
                ('experience_description', models.CharField(choices=[('hs', 'I am a former High School Mock Trial Competitor'), ('college', 'I am a current or former College Mock Trial Competitor'), ('ls', 'I am a current or former Law School Mock Trial Competitor')], help_text='Do you have any experience competing in high school, collegiate or law school mock trial competitions?', max_length=40)),
                ('judged_rounds', models.IntegerField(choices=[(1, 'I have judged 1-2 Mock Trial Competitions in the past'), (2, 'I have judged 3-5 Mock Trial Competitions in the past'), (3, 'I have judged 5 or more Mock Trial Competitions in the past')], help_text='Do you have any experience judging high school, collegiate or law school mock trial competitions?')),
                ('affiliations', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField(blank=True, max_length=5000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParadigmPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('att', 'Attorney'), ('wit', 'Witness')], max_length=40)),
                ('low_end', models.CharField(blank=True, max_length=40, null=True)),
                ('high_end', models.CharField(blank=True, max_length=40, null=True)),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paradigm_preferences', related_query_name='paradigm_preference', to='tourney.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='ParadigmPreferenceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('paradigm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', related_query_name='preference_scale', to='submission.paradigm')),
                ('paradigm_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paradigm_preference_items', related_query_name='paradigm_preference_items', to='submission.paradigmpreference')),
            ],
        ),
    ]
