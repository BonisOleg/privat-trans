from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_proof", "0002_review_source"),
    ]

    operations = [
        migrations.CreateModel(
            name="GalleryWork",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="gallery/")),
                ("alt_uk", models.CharField(max_length=180)),
                ("alt_en", models.CharField(blank=True, max_length=180)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Фото галереї",
                "verbose_name_plural": "Галерея робіт",
                "ordering": ["order", "id"],
            },
        ),
    ]
