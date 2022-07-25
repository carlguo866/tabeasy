# Generated by Django 3.2.14 on 2022-07-25 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourney', '0016_auto_20220724_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='d_close_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit1_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit1_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit1_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit1_wit_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit2_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit2_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit2_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit2_wit_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit3_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit3_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit3_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='d_wit3_wit_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_close_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit1_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit1_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit1_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit2_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit2_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit2_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit2_wit_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit3_att_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit3_att_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit3_wit_cross_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='ballot',
            name='p_wit3_wit_direct_comment',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
