# Generated by Django 4.1.3 on 2022-11-20 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0019_alter_dictionary_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='lang_from',
            field=models.CharField(default='EN', max_length=3),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='lang_to',
            field=models.CharField(default='RU', max_length=3),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='level',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], max_length=2),
        ),
    ]
