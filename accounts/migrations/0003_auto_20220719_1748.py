# Generated by Django 3.2.14 on 2022-07-20 00:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220718_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='ballots',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='cs',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='division',
            field=models.CharField(default='Division', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='pd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='sides',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), null=True, size=4),
        ),
        migrations.AddField(
            model_name='team',
            name='team_roster',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), null=True, size=10),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
