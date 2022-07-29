# Generated by Django 3.2.14 on 2022-07-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0034_round_submit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='conflicts',
            field=models.ManyToManyField(blank=True, to='tourney.Team'),
        ),
        migrations.AlterField(
            model_name='judge',
            name='judge_friends',
            field=models.ManyToManyField(blank=True, related_name='_tourney_judge_judge_friends_+', to='tourney.Judge'),
        ),
    ]
