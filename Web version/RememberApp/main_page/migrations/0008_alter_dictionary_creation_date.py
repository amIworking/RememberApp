# Generated by Django 4.1.2 on 2022-10-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0007_alter_dictionary_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictionary',
            name='creation_date',
            field=models.CharField(default='27.10.2022 13:50', max_length=40),
        ),
    ]