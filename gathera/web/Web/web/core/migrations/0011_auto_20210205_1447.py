# Generated by Django 3.0.5 on 2021-02-05 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210205_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographics',
            name='age_other',
            field=models.CharField(default=-1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demographics',
            name='education_other',
            field=models.CharField(default=-1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demographics',
            name='gender_other',
            field=models.CharField(default=-1, max_length=512),
            preserve_default=False,
        ),
    ]
