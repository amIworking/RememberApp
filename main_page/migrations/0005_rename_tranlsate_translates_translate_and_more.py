# Generated by Django 4.1.2 on 2022-10-24 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0004_alter_dictionary_creation_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='translates',
            old_name='tranlsate',
            new_name='translate',
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='creation_date',
            field=models.DateTimeField(default='24.10.2022 15:16'),
        ),
    ]
