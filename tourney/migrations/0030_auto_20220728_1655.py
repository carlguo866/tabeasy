# Generated by Django 3.2.14 on 2022-07-28 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0029_auto_20220728_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captainsmeeting',
            name='character_evidence_option1_description',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='character_evidence_option2_description',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='character_evidence_option3_description',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='character_evidence_option4_description',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
