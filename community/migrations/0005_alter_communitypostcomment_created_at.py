# Generated by Django 5.1.3 on 2024-12-15 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0004_communitypostcomment_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communitypostcomment",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
