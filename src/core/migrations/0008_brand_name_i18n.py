from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_home_body_cms"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sitesettings",
            old_name="brand_name",
            new_name="brand_name_uk",
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="brand_name_en",
            field=models.CharField(blank=True, default="PRIVAT-TRANS", max_length=80),
        ),
    ]
