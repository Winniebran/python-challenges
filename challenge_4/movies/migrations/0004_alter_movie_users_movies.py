# Generated by Django 4.1.6 on 2023-02-17 23:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movies", "0003_movieorder_movie_users_movies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="users_movies",
            field=models.ManyToManyField(
                related_name="users_movies",
                through="movies.MovieOrder",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
