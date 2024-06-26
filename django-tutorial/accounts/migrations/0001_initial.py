# Generated by Django 5.0.2 on 2024-04-06 13:07

import accounts.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("mobile", models.CharField(max_length=32, null=True, unique=True)),
                ("wechat_id", models.CharField(max_length=256, null=True, unique=True)),
                ("email", models.CharField(max_length=64, null=True, unique=True)),
                ("password", models.TextField(null=True)),
                ("emai_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PasswordResetter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        default=accounts.models.generate_token,
                        max_length=64,
                        unique=True,
                    ),
                ),
                ("expires_in", models.IntegerField(default=10800)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
    ]
