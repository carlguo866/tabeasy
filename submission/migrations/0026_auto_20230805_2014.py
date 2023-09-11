# Generated by Django 3.2.14 on 2023-08-06 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0025_alter_spirit_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='spirit',
            name='q1',
            field=models.TextField(blank=True, help_text='Please list any reasons that you think one of the teams you competed against is especially deserving of the Spirit Award. Please provide a specific example, if possible.', max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='spirit',
            name='q2',
            field=models.TextField(blank=True, help_text="Please list any team that you didn’t compete against but that you believe exhibited mock trial's ideals and, therefore, should receive additional consideration for the Spirit Award. Please provide a specific example.", max_length=5000, null=True),
        ),
    ]