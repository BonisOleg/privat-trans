# Generated manually for homepage body + site chrome CMS sections

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_fleet_page_cms"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeGeographySettings",
            fields=[],
            options={
                "verbose_name": "Головна — Географія",
                "verbose_name_plural": "Головна — Географія",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeRoutesSettings",
            fields=[],
            options={
                "verbose_name": "Головна — Маршрути",
                "verbose_name_plural": "Головна — Маршрути",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeMidSettings",
            fields=[],
            options={
                "verbose_name": "Головна — Послуги та автопарк",
                "verbose_name_plural": "Головна — Послуги та автопарк",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeExperienceSettings",
            fields=[],
            options={
                "verbose_name": "Головна — Переваги та процес",
                "verbose_name_plural": "Головна — Переваги та процес",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.CreateModel(
            name="HomeSocialSettings",
            fields=[],
            options={
                "verbose_name": "Головна — Калькулятор і соцблок",
                "verbose_name_plural": "Головна — Калькулятор і соцблок",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.CreateModel(
            name="SiteChromeSettings",
            fields=[],
            options={
                "verbose_name": "Сайт — CTA та форма",
                "verbose_name_plural": "Сайт — CTA та форма",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
    ]
