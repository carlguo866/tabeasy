# Generated by Django 3.2.14 on 2023-09-11 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0026_auto_20230805_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='side',
            field=models.CharField(choices=[('P', 'Prosecution/Plaintiff'), ('D', 'Defense'), ('other', 'Swing')], max_length=5, null=True),
        ),
    ]