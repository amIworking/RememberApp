# Generated by Django 4.1.3 on 2022-11-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0015_alter_dictionary_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dictionary',
            old_name='owner_id',
            new_name='owner',
        ),
        migrations.AddField(
            model_name='dictionary',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='lang_from',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='lang_to',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]