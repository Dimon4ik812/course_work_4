# Generated by Django 5.1.1 on 2024-11-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_customsuser_options_customsuser_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customsuser",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="photo/avatars/"),
        ),
    ]
