# Generated by Django 3.2.14 on 2022-07-22 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0010_alter_round_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Round',
            new_name='PairingItem',
        ),
    ]
