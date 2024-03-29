# Generated by Django 2.2.4 on 2019-09-05 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('key', 'location')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=50)),
                ('detailed', models.CharField(max_length=1000)),
                ('dev_instructions', models.CharField(max_length=2000)),
            ],
            options={
                'unique_together': {('key', 'language')},
            },
        ),
    ]
