# Generated by Django 3.0.5 on 2021-02-05 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_demographics'),
    ]

    operations = [
        migrations.AddField(
            model_name='demographics',
            name='education',
            field=models.CharField(default='na', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demographics',
            name='gender',
            field=models.CharField(default='na', max_length=512),
            preserve_default=False,
        ),
    ]