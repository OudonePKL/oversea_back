# Generated by Django 5.0.2 on 2024-02-11 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=100, unique=True, verbose_name="Email Address"
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="nickname"
                    ),
                ),
                (
                    "profile_image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="media/",
                        verbose_name="profile image",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("is_staff", models.BooleanField(default=False, verbose_name="Staff")),
                ("is_client", models.BooleanField(default=True, verbose_name="Client")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False, verbose_name="Owner Or Developer"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "1. User information",
            },
        ),
        migrations.CreateModel(
            name="CheckEmail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=100, verbose_name="Email for verification"
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="code for confirmation"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
            ],
            options={
                "verbose_name_plural": "2. Authentication code management",
            },
        ),
    ]
