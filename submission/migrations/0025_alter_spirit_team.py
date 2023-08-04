# Generated by Django 3.2.14 on 2023-08-04 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0026_auto_20230804_0212'),
        ('submission', '0024_auto_20230803_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spirit',
            name='team',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='spirit', serialize=False, to='tourney.team'),
        ),
    ]
