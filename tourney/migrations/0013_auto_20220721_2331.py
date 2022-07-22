# Generated by Django 3.2.14 on 2022-07-22 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0012_auto_20220721_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pairingitem',
            name='judge_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pairing1s', related_query_name='pairing1', to='tourney.judge'),
        ),
        migrations.AlterField(
            model_name='pairingitem',
            name='judge_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pairing2s', related_query_name='pairing2', to='tourney.judge'),
        ),
    ]
