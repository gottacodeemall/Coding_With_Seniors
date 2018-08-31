# Generated by Django 2.1 on 2018-08-31 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('solution', models.TextField(null=True)),
                ('solution_url', models.URLField(blank=True, null=True)),
                ('liked_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('date', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerSessionUserLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('url_problem', models.URLField(null=True)),
                ('solution', models.CharField(blank=True, max_length=255, null=True)),
                ('url_solution', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
                ('date', models.DateField(null=True)),
                ('description', models.TextField(null=True)),
                ('test_name', models.CharField(blank=True, max_length=255, null=True)),
                ('test_url', models.URLField(blank=True, null=True)),
                ('top_coder', models.CharField(blank=True, max_length=255, null=True)),
                ('top_contributor', models.CharField(blank=True, max_length=255, null=True)),
                ('top_improver', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='ranking',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Session'),
        ),
        migrations.AddField(
            model_name='ranking',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='problem',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Session'),
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, to='events.Tags'),
        ),
        migrations.AddField(
            model_name='persessionuserlikes',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Session'),
        ),
        migrations.AddField(
            model_name='persessionuserlikes',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_profile.UserProfile'),
        ),
        migrations.AddField(
            model_name='editorial',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Problem'),
        ),
        migrations.AddField(
            model_name='editorial',
            name='user_submitted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.UserProfile'),
        ),
    ]
