# Generated by Django 4.1.3 on 2022-11-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
