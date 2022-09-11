# Generated by Django 3.2.14 on 2022-09-11 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0007_auto_20220908_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitors', related_query_name='competitor', to='tourney.team'),
        ),
    ]
