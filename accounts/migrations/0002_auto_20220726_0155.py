# Generated by Django 3.2.14 on 2022-07-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_judge',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_team',
            field=models.BooleanField(default=False),
        ),
    ]
