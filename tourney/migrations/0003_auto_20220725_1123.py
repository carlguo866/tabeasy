# Generated by Django 3.1.1 on 2022-07-25 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0002_auto_20220725_1117'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together={('round', 'judge')},
        ),
    ]
