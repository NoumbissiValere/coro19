# Generated by Django 2.2 on 2020-04-10 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=10)),
                ('path', models.CharField(max_length=80)),
                ('status', models.IntegerField()),
                ('time', models.CharField(max_length=100)),
            ],
        ),
    ]
