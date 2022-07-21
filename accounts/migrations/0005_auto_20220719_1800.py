# Generated by Django 3.2.14 on 2022-07-20 01:00

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_team_team_roster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='sides',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=1), blank=True, null=True, size=4),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_roster',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=10),
        ),
    ]
