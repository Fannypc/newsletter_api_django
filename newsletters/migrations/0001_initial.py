# Generated by Django 2.2.14 on 2020-12-22 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=50, null=True)),
                ('frequency', models.CharField(max_length=50, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('guests', models.ManyToManyField(blank=True, related_name='guests', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL)),
                ('target', models.ManyToManyField(blank=True, related_name='target', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('is_admin', 'Is Admin'), ('is_user', 'Is User'), ('is_owner', 'Is Owner'), ('is_guest', 'Is Guest')),
            },
        ),
    ]
