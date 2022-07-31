# Generated by Django 3.2.14 on 2022-07-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0036_remove_round_submit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pairing',
            old_name='submit',
            new_name='final_submit',
        ),
        migrations.RemoveField(
            model_name='captainsmeeting',
            name='poole_pronoun',
        ),
        migrations.AddField(
            model_name='pairing',
            name='team_submit',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='bowman_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Whit Bowman', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='floyd_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Haley Floyd', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='hunter_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Jackie Hunter', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='isaacs_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Billie Issacs', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='kaminsky_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Charlie Kaminsky', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='kimball_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='Francis Kimball', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='captainsmeeting',
            name='longstreet_pronoun',
            field=models.CharField(choices=[('he', 'He/Him'), ('she', 'She/Her'), ('they', 'They/Them'), ('ze', 'Ze/Hir')], help_text='J.C. Longstreet', max_length=30, null=True),
        ),
    ]
