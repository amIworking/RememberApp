# Generated by Django 4.1.3 on 2022-11-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0017_alter_dictionary_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictionary',
            name='level',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='dictionary',
            name='raiting',
            field=models.IntegerField(null=True),
        ),
    ]
