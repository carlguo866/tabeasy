# Generated by Django 3.2.14 on 2023-08-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0022_alter_competitor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='spirit_award',
            field=models.BooleanField(default=False),
        ),
    ]
