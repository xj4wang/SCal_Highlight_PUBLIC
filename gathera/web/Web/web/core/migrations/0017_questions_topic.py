# Generated by Django 3.0.5 on 2021-02-07 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20210205_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='topic',
            field=models.CharField(default='na', max_length=512),
            preserve_default=False,
        ),
    ]
