# Generated by Django 3.1.7 on 2022-04-02 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_team_stripe_customer_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="stripe_subscription_id",
            field=models.CharField(default="", max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
