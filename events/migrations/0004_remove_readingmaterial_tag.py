# Generated by Django 2.1 on 2018-09-01 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_readingmaterial_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readingmaterial',
            name='tag',
        ),
    ]
