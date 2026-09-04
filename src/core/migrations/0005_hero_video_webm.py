from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_home_scenarios_cms"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_video_webm",
            field=models.FileField(blank=True, upload_to="hero/"),
        ),
    ]
