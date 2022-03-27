# Generated by Django 3.1.7 on 2022-03-26 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220326_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_token',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
