# Generated by Django 3.2.14 on 2022-07-22 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0009_auto_20220721_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
