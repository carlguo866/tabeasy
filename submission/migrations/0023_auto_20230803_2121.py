# Generated by Django 3.2.14 on 2023-08-04 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0022_spirit_submit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spirit',
            old_name='round1_spirit',
            new_name='round1',
        ),
        migrations.RenameField(
            model_name='spirit',
            old_name='round2_spirit',
            new_name='round2',
        ),
        migrations.RenameField(
            model_name='spirit',
            old_name='round3_spirit',
            new_name='round3',
        ),
        migrations.RenameField(
            model_name='spirit',
            old_name='round4_spirit',
            new_name='round4',
        ),
    ]
