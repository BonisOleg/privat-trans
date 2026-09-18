from datetime import date

from django.core.management.base import BaseCommand

from src.careers.models import Vacancy
from src.core.models import PageSEO, SiteBlock, SiteSettings
from src.faq.models import FaqItem
from src.services.models import Service
from src.pages.gallery import seed_gallery_works
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

LARDI_REVIEWS_URL = (
    "https://lardi-trans.com/log/user/15009884246/responses/?scopeType=POSITIVE"
)

REVIEWS = [
    {
        "author": '"Всеукраїнська брокерська агенція", ТОВ',
        "flag": "FR → UA · Loison-sous-Lens — Бородянка",
        "quote_uk": (
            "Дуже задоволені співпрацею з перевізником! Вантаж був доставлений вчасно "
            "й у повній цілісності. Окреме дякуємо Станіславу за оперативний зв’язок, "
            "відповідальний підхід та професійність на всіх етапах роботи. Рекомендуємо "
            "до співпраці!"
        ),
        "quote_en": (
            "Very happy with this carrier! The cargo arrived on time and fully intact. "
            "Special thanks to Stanislav for prompt contact, a responsible approach and "
            "professionalism at every stage. We recommend working with them!"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2026, 7, 20),
        "order": 1,
    },
    {
        "author": "Рибак Н.В., ФОП",
        "flag": "DE → UA · Шмісберг — Київ",
        "quote_uk": "Дякуємо за співпрацю! Бажаємо успіху! Рекомендуємо!",
        "quote_en": "Thank you for the cooperation! We wish you success! Recommended!",
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2026, 5, 27),
        "order": 2,
    },
    {
        "author": "Мар'юсік Катерина Борисівна, ФОП",
        "flag": "FR → UA · Карвен — Вишневе",
        "quote_uk": "Все згідно домовленостей! Рекомендуємо до співпраці!",
        "quote_en": "Everything as agreed! We recommend working with them!",
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 11, 3),
        "order": 3,
    },
    {
        "author": "Комишев Дмитро Миколайович, ФОП",
        "flag": "PL → UA · Варшава — Київ",
        "quote_uk": (
            "Дякуємо за співпрацю! Станістав увесь час був на звязку, все швидко чітко "
            "згідно домовленостей! Надійний вантажовідправник! Рекомендуємо та "
            "сподіваємось на подальшу співпрацю!)"
        ),
        "quote_en": (
            "Thank you for the cooperation! Stanislav stayed in touch the whole time — "
            "fast, clear and as agreed! A reliable shipper! We recommend them and hope "
            "to keep working together!)"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 9, 12),
        "order": 4,
    },
    {
        "author": "Granit Group",
        "flag": "FR → UA · Saint-Pierre-lès-Elbeuf — Київ",
        "quote_uk": (
            "Все пройшло чудово, вантаж доставили швидко та без проблем, дякую "
            "Станіславу за відмінну роботу. Рекомендую!!!"
        ),
        "quote_en": (
            "Everything went great, the cargo was delivered quickly and without issues. "
            "Thank you, Stanislav, for excellent work. Recommended!!!"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 8, 12),
        "order": 5,
    },
    {
        "author": "НЕОЛИТ",
        "flag": "FR → UA · Карвен — Львів",
        "quote_uk": (
            "Робота виконана дуже професійно!!!!!Дякую за співпрацю!!!!Дякую Станіславу!!!!"
        ),
        "quote_en": (
            "The work was done very professionally!!!!! Thank you for the cooperation!!!! "
            "Thank you, Stanislav!!!!"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 6, 23),
        "order": 6,
    },
    {
        "author": "Gia grupė MB",
        "flag": "BE → UA · Gent — Київ",
        "quote_uk": (
            "Хороший перевізник, вперше робили збірне перевезення — досвід позитивний. "
            "Продовжимо співпрацю. Рекомендую компанію."
        ),
        "quote_en": (
            "Good hauler, first time I did an LTL hauling, and it was a good experience. "
            "We will keep working. I recommend the transportation company"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 6, 12),
        "order": 7,
    },
    {
        "author": "Ель Логістик, ТОВ",
        "flag": "DE → UA · Берлін — Київ",
        "quote_uk": (
            "Дякую Владиславу за організацію перевезення, все було в рамках домовленостей, "
            "швидко та професійно. Рекомендую до співпраці!"
        ),
        "quote_en": (
            "Thanks to Vladyslav for organizing the shipment — everything was as agreed, "
            "fast and professional. I recommend working with them!"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 5, 9),
        "order": 8,
    },
    {
        "author": "Кондратюк Олена Валеріївна, ФОП",
        "flag": "UA → FR · Зоря — Петерсбак",
        "quote_uk": (
            "Дякуємо за співпрацю! Робота виконана якісно, оплата вчасна, відмінна "
            "комунікація! Все супер, окрема поляка Станіславу! Будемо працювати й далі)"
        ),
        "quote_en": (
            "Thank you for the cooperation! Quality work, on-time payment and excellent "
            "communication! All great, special thanks to Stanislav! We will keep working "
            "together)"
        ),
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 4, 24),
        "order": 9,
    },
    {
        "author": "Штик Аліна Петрівна, ФОП",
        "flag": "BE → UA · Генк — Київ",
        "quote_uk": "Хороший вантажовідправник, все відповідально і вчасно, рекомендую",
        "quote_en": "A good shipper — responsible and on time. I recommend them",
        "source": "Lardi-Trans",
        "source_url": LARDI_REVIEWS_URL,
        "reviewed_on": date(2025, 1, 23),
        "order": 10,
    },
]


SEO = [
    (
        "home",
        "ПРИВАТ-ТРАНС — комплексна доставка Європа ↔️ Україна ↔️ Азія",
        "PRIVAT-TRANS — freight Europe ↔ Ukraine ↔ Asia",
        "Міжнародні перевезення 10 кг–23 т: Європа, Україна, Азія. Склади в ЄС, митниця, страхування. Залиште заявку онлайн.",
        "International freight 10 kg–23 t across Europe, Ukraine and Asia. EU warehouses, customs and insurance. Request a quote.",
    ),
    (
        "about",
        "Про нас — ПРИВАТ-ТРАНС з 2007 року",
        "About PRIVAT-TRANS — since 2007",
        "ПП ПРИВАТ-ТРАНС: експедиція та виконання рейсів з 2007 року. Власний автопарк, склади в Європі, митниця і страхування вантажу.",
        "PE PRIVAT-TRANS: freight forwarding and haulage since 2007. Own fleet, EU warehouses, customs and cargo insurance.",
    ),
    (
        "fleet",
        "Автопарк — ПРИВАТ-ТРАНС",
        "Fleet — PRIVAT-TRANS",
        "Тенти 86–120 м², рефрижератори, ізотерми, ADR і негабарит. 10 кг–23 т на рейсах Європа — Україна — Азія.",
        "Tautliners 86–120 m², reefers, isotherms, ADR and oversized cargo. 10 kg–23 t on Europe–Ukraine–Asia lanes.",
    ),
    (
        "services",
        "Послуги міжнародних перевезень",
        "International freight services",
        "Збірні від 10 кг, FTL до 23 т, контейнери, склади, митне оформлення та страхування. Вісім послуг під ключ.",
        "Groupage from 10 kg, FTL up to 23 t, containers, warehousing, customs and insurance. Eight turnkey services.",
    ),
    (
        "faq",
        "Питання про перевезення — ПРИВАТ-ТРАНС",
        "Freight FAQ — PRIVAT-TRANS",
        "Мінімальна вага, частота рейсів, документи, страхування та що входить у доставку під ключ. Відповіді експедитора.",
        "Minimum weight, departure frequency, documents, insurance and what turnkey delivery includes.",
    ),
    (
        "calculator",
        "Калькулятор орієнтовної вартості",
        "Indicative freight calculator",
        "Орієнтовний діапазон вартості перевезення за вагою, об’ємом і типом кузова. Не оферта — менеджер підтвердить тариф.",
        "Indicative freight range by weight, volume and body type. Not an offer — a manager confirms the rate.",
    ),
    (
        "contacts",
        "Контакти ПП ПРИВАТ-ТРАНС, Рівне",
        "Contact PE PRIVAT-TRANS, Rivne",
        "Рівне, вул. Відінська, 10. Телефон, email і форма заявки на міжнародне перевезення. ПП ПРИВАТ-ТРАНС.",
        "Rivne, Vidinska St. 10. Phone, email and a quote form for international freight. PE PRIVAT-TRANS.",
    ),
    (
        "privacy",
        "Політика конфіденційності",
        "Privacy policy",
        "Як ПП ПРИВАТ-ТРАНС обробляє персональні дані з форм заявок і комунікації. Підстава — згода та договір.",
        "How PE PRIVAT-TRANS processes personal data from quote forms and communication. Legal basis: consent and contract.",
    ),
]


class Command(BaseCommand):
    help = "Idempotent demo content for PRIVAT-TRANS"

    def handle(self, *args, **options):
        settings = SiteSettings.load()
        settings.slogan_uk = "Ваш надійний партнер"
        settings.slogan_en = "Your reliable partner"
        if not settings.map_embed_url or "openstreetmap.org" in settings.map_embed_url:
            settings.map_embed_url = (
                "https://www.google.com/maps"
                "?q=50.6140963,26.2743911"
                "&hl=uk&z=16&output=embed"
            )
        settings.save(update_fields=["slogan_uk", "slogan_en", "map_embed_url"])
        from src.core.block_defaults import BLOCK_DEFAULTS
        from src.core.site_blocks import invalidate_site_blocks_cache, seed_default_blocks

        seed_default_blocks()
        wrap_keys = ("hero_badge", "hero_badge_rest", "hero_fact_rest", "hero_form_title")
        for key in wrap_keys:
            meta = BLOCK_DEFAULTS[("home", key)]
            SiteBlock.objects.filter(page="home", key=key).update(
                text_uk=meta["text_uk"],
                text_en=meta["text_en"],
            )
        invalidate_site_blocks_cache()
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
        keep_authors = [item["author"] for item in REVIEWS]
        Review.objects.exclude(author__in=keep_authors).delete()
        for item in REVIEWS:
            Review.objects.update_or_create(
                author=item["author"],
                defaults={
                    "quote_uk": item["quote_uk"],
                    "quote_en": item["quote_en"],
                    "flag": item["flag"],
                    "source": item.get("source", ""),
                    "source_url": item.get("source_url", ""),
                    "reviewed_on": item.get("reviewed_on"),
                    "order": item["order"],
                    "is_published": True,
                },
            )
        for index, name in enumerate(["Partner A", "Partner B", "Partner C", "Partner D"], start=1):
            Partner.objects.update_or_create(name=name, defaults={"order": index})
        seed_gallery_works()
        for slug, title_uk, title_en, desc_uk, desc_en in SEO:
            PageSEO.objects.update_or_create(
                slug=slug,
                defaults={
                    "title_uk": title_uk,
                    "title_en": title_en,
                    "description_uk": desc_uk,
                    "description_en": desc_en,
                    "h1_uk": "",
                    "h1_en": "",
                },
            )
        self.stdout.write(self.style.SUCCESS("seed_demo ok"))
