# Generated by Django 3.0.5 on 2021-02-05 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_auto_20210205_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('na', 'I prefer not to answer.')], max_length=512)),
                ('q2', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('na', 'I prefer not to answer.')], max_length=512)),
                ('q3', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('na', 'I prefer not to answer.')], max_length=512)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]