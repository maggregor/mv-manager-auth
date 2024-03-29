# Generated by Django 3.1.7 on 2022-03-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_create_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="picture",
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="access_token",
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="refresh_token",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
