from django.core.management.base import BaseCommand

from src.careers.models import Vacancy
from src.core.models import PageSEO, SiteSettings
from src.faq.models import FaqItem
from src.services.models import Service
from src.social_proof.models import Partner, Review

SERVICES = [
    {
        "slug": "mizhnarodni-perevezennya",
        "title_uk": "Міжнародні перевезення",
        "title_en": "International freight",
        "teaser_uk": "Експорт/імпорт, 10 кг–23 т, Європа та Азія.",
        "teaser_en": "Export/import, 10 kg–23 t, Europe and Asia.",
        "body_uk": "Комплексна доставка вантажів Європа ↔️ Україна ↔️ Азія з повним логістичним супроводом.",
        "body_en": "End-to-end freight Europe ↔ Ukraine ↔ Asia.",
        "icon_key": "globe",
        "order": 1,
    },
    {
        "slug": "zbirni-vid-10-kg",
        "title_uk": "Збірний вантаж (LTL) від 10кг",
        "title_en": "Groupage (LTL) from 10 kg",
        "teaser_uk": "Регулярні щотижневі рейси з країн Європи та Азії. Ви платите виключно за місце, яке займає ваш товар на палеті, без переплати за пусту машину.",
        "teaser_en": "Regular weekly departures from Europe and Asia. You pay only for the pallet space your goods occupy — no charge for empty truck capacity.",
        "body_uk": (
            "Збірний вантаж (LTL) від 10кг. "
            "Регулярні щотижневі рейси з країн Європи та Азії. "
            "Ви платите виключно за місце, яке займає ваш товар на палеті, без переплати за пусту машину."
        ),
        "body_en": (
            "Groupage (LTL) from 10 kg. "
            "Regular weekly departures from Europe and Asia. "
            "You pay only for the pallet space your goods occupy — no charge for empty truck capacity."
        ),
        "icon_key": "boxes",
        "order": 2,
    },
    {
        "slug": "povne-avto-ftl",
        "title_uk": "Повне авто (FTL) до 23 тонн",
        "title_en": "Full truck (FTL) up to 23 tonnes",
        "teaser_uk": (
            "FTL перевезення: тенти(86-120 м2) для загальних комерційних вантажів, "
            "рефрижератори та ізотерми для товарів, що потребують температурного режиму(продукти, медикаменти). "
            "Небезпечні (ADR) та негабаритні вантажі. Перевезення виставкових вантажів."
        ),
        "teaser_en": (
            "FTL: tautliners (86–120 m²) for general commercial cargo, "
            "reefers and isotherms for temperature-controlled goods (food, medicines). "
            "ADR and oversized cargo. Exhibition freight."
        ),
        "body_uk": (
            "FTL перевезення: тенти(86-120 м2) для загальних комерційних вантажів, "
            "рефрижератори та ізотерми для товарів, що потребують температурного режиму(продукти, медикаменти). "
            "Небезпечні (ADR) та негабаритні вантажі. Перевезення виставкових вантажів."
        ),
        "body_en": (
            "FTL: tautliners (86–120 m²) for general commercial cargo, "
            "reefers and isotherms for temperature-controlled goods (food, medicines). "
            "ADR and oversized cargo. Exhibition freight."
        ),
        "icon_key": "truck",
        "order": 3,
    },
    {
        "slug": "specvantazhi",
        "title_uk": "Спецвантажі",
        "title_en": "Special cargo",
        "teaser_uk": "Температурний режим, небезпечні (ADR), негабарит.",
        "teaser_en": "Temperature-controlled, ADR, oversized.",
        "body_uk": "Перевезення товарів, що потребують температурного режиму, ADR та негабаритних партій.",
        "body_en": "Temperature-controlled, ADR and oversized shipments.",
        "icon_key": "alert",
        "order": 4,
    },
    {
        "slug": "kontejnery",
        "title_uk": "Контейнери",
        "title_en": "Containers",
        "teaser_uk": "Мультимодал: море + авто, документи на весь ланцюг.",
        "teaser_en": "Multimodal sea + road, documents for the full chain.",
        "body_uk": "Контейнерні перевезення море + авто з документами на весь ланцюг.",
        "body_en": "Sea + road container logistics with end-to-end documents.",
        "icon_key": "container",
        "order": 5,
    },
    {
        "slug": "vlasni-sklady",
        "title_uk": "Під ключ: склади перетримки та консолідації в Європі",
        "title_en": "Turnkey: storage and consolidation warehouses in Europe",
        "teaser_uk": "Відповідальне зберігання, перетарка, маркування, палетування та пакування ваших товарів на європейських складах.",
        "teaser_en": "Responsible storage, re-packing, labeling, palletizing and packaging of your goods at European warehouses.",
        "body_uk": "Відповідальне зберігання, перетарка, маркування, палетування та пакування ваших товарів на європейських складах.",
        "body_en": "Responsible storage, re-packing, labeling, palletizing and packaging of your goods at European warehouses.",
        "icon_key": "warehouse",
        "order": 6,
    },
    {
        "slug": "mytne-oformlennya",
        "title_uk": "Митно-брокерські послуги",
        "title_en": "Customs brokerage",
        "teaser_uk": "Консультації та оформлення транзитних (Т1, Т2) та експортних (EX1) декларацій в Європі, повне митне очищення.",
        "teaser_en": "Advice and filing of transit (T1, T2) and export (EX1) declarations in Europe, full customs clearance.",
        "body_uk": "Консультації та оформлення транзитних (Т1, Т2) та експортних (EX1) декларацій в Європі, повне митне очищення.",
        "body_en": "Advice and filing of transit (T1, T2) and export (EX1) declarations in Europe, full customs clearance.",
        "icon_key": "docs",
        "order": 7,
    },
    {
        "slug": "strahuvannya",
        "title_uk": "Страхування",
        "title_en": "Insurance",
        "teaser_uk": "Обов’язкове страхування вантажу: фінансовий і юридичний захист.",
        "teaser_en": "Mandatory cargo insurance: financial and legal cover.",
        "body_uk": "Страхуємо вантаж і авто. Повний фінансовий та юридичний захист вашого майна.",
        "body_en": "Cargo and vehicle insurance with full financial and legal cover.",
        "icon_key": "shield",
        "order": 8,
    },
]

FAQ = [
    ("Яка мінімальна вага?", "What is the minimum weight?", "Збірні від 10 кг. Ви платите за місце на палеті.", "LTL from 10 kg. You pay for pallet space."),
    ("Як часто ходять рейси?", "How often do you depart?", "Регулярні щотижневі рейси з країн Європи та Азії.", "Weekly groupage from Europe and Asia."),
    ("Що входить у «під ключ»?", "What is included in turnkey?", "Склади в Європі, митниця (Т1/Т2, EX1), страхування і доставка.", "EU warehouses, customs (T1/T2, EX1), insurance and delivery."),
    ("Чи страхуєте вантаж?", "Do you insure cargo?", "Так, обов’язкове страхування вантажу і авто.", "Yes — mandatory cargo and vehicle insurance."),
    ("Які документи потрібні?", "Which documents are needed?", "Інвойс, пакувальний лист, коди УКТЗЕД і довіреність — менеджер надішле чекліст.", "Invoice, packing list, HS codes and a power of attorney."),
]

SEO = [
    ("home", "ПРИВАТ-ТРАНС — комплексна доставка Європа ↔️ Україна ↔️ Азія", "PRIVAT-TRANS — freight Europe ↔ Ukraine ↔ Asia"),
    ("about", "Про нас — ПРИВАТ-ТРАНС з 2007 року", "About PRIVAT-TRANS — since 2007"),
    ("fleet", "Автопарк — ПРИВАТ-ТРАНС", "Fleet — PRIVAT-TRANS"),
    ("services", "Послуги міжнародних перевезень", "International freight services"),
    ("faq", "Питання про перевезення — ПРИВАТ-ТРАНС", "Freight FAQ — PRIVAT-TRANS"),
    ("calculator", "Калькулятор орієнтовної вартості", "Indicative freight calculator"),
    ("contacts", "Контакти ПП ПРИВАТ-ТРАНС, Рівне", "Contact PE PRIVAT-TRANS, Rivne"),
    ("privacy", "Політика конфіденційності", "Privacy policy"),
]


class Command(BaseCommand):
    help = "Idempotent demo content for PRIVAT-TRANS"

    def handle(self, *args, **options):
        settings = SiteSettings.load()
        settings.slogan_uk = "Ваш надійний партнер"
        settings.save(update_fields=["slogan_uk"])
        from src.core.site_blocks import seed_default_blocks

        seed_default_blocks()
        for item in SERVICES:
            Service.objects.update_or_create(slug=item["slug"], defaults=item)
        for index, (q_uk, q_en, a_uk, a_en) in enumerate(FAQ, start=1):
            FaqItem.objects.update_or_create(
                question_uk=q_uk,
                defaults={
                    "question_en": q_en,
                    "answer_uk": a_uk,
                    "answer_en": a_en,
                    "order": index,
                    "show_on_home": index <= 5,
                    "is_published": True,
                },
            )
        Vacancy.objects.exclude(title_uk__in=["Менеджер з логістики", "Спеціаліст митного оформлення"]).delete()
        Vacancy.objects.update_or_create(
            title_uk="Менеджер з логістики",
            defaults={
                "title_en": "Logistics manager",
                "text_uk": "Персональний супровід маршрутів Європа / Азія.",
                "text_en": "Personal handling of Europe / Asia lanes.",
                "order": 1,
            },
        )
        Vacancy.objects.update_or_create(
            title_uk="Спеціаліст митного оформлення",
            defaults={
                "title_en": "Customs specialist",
                "text_uk": "Т1, Т2, EX1 та повне очищення.",
                "text_en": "T1, T2, EX1 and full clearance.",
                "order": 2,
            },
        )
        Review.objects.update_or_create(
            author="ТОВ «Приклад»",
            defaults={
                "quote_uk": "Стабільні щотижневі збірні, без сюрпризів на кордоні.",
                "quote_en": "Reliable weekly groupage, no border surprises.",
                "flag": "Приклад відгуку",
                "order": 1,
            },
        )
        for index, name in enumerate(["Partner A", "Partner B", "Partner C", "Partner D"], start=1):
            Partner.objects.update_or_create(name=name, defaults={"order": index})
        for slug, title_uk, title_en in SEO:
            PageSEO.objects.update_or_create(
                slug=slug,
                defaults={
                    "title_uk": title_uk,
                    "title_en": title_en,
                    "description_uk": title_uk,
                    "description_en": title_en,
                    "h1_uk": "",
                    "h1_en": "",
                },
            )
        self.stdout.write(self.style.SUCCESS("seed_demo ok"))
