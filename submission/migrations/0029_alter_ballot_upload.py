# Generated by Django 3.2.14 on 2023-09-16 16:11

from django.db import migrations, models
import submission.models.ballot


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0028_remove_spirit_round4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to=submission.models.ballot.user_directory_path),
        ),
    ]
