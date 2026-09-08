# Generated manually for Fleet CMS page

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_hero_video_webm"),
    ]

    operations = [
        migrations.CreateModel(
            name="FleetPageSettings",
            fields=[],
            options={
                "verbose_name": "Автопарк",
                "verbose_name_plural": "Автопарк",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="page",
            field=models.CharField(
                choices=[
                    ("home", "Головна"),
                    ("about", "Про нас"),
                    ("fleet", "Автопарк"),
                    ("contacts", "Контакти"),
                    ("privacy", "Політика"),
                    ("services", "Послуги"),
                    ("faq", "FAQ"),
                    ("calculator", "Калькулятор"),
                    ("site", "Сайт"),
                ],
                max_length=32,
            ),
        ),
    ]
