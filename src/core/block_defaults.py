"""Defaults and labels for SiteBlock CMS keys."""

from __future__ import annotations

from src.core.block_defaults_fleet import (
    FLEET_BLOCK_DEFAULTS,
    FLEET_INLINE_KEYS,
    FLEET_MULTILINE_KEYS,
    FLEET_TINYMCE_KEYS,
)
from src.core.block_defaults_home_body import HOME_BODY_BLOCK_DEFAULTS

BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    # —— Home / Hero ——
    ("home", "hero_section_visible"): {
        "label": "Показувати Hero на головній",
        "content_type": "text",
        "text_uk": "1",
        "text_en": "1",
        "sort_order": 0,
    },
    ("home", "hero_badge"): {
        "label": "Badge — перший рядок",
        "content_type": "text",
        "text_uk": "Комплексна доставка вантажів",
        "text_en": "End-to-end freight",
        "sort_order": 10,
    },
    ("home", "hero_badge_rest"): {
        "label": "Badge — з «Європа»",
        "content_type": "text",
        "text_uk": "Європа ↔️ Україна ↔️ Азія",
        "text_en": "Europe ↔ Ukraine ↔ Asia",
        "sort_order": 11,
    },
    ("home", "hero_title"): {
        "label": "Заголовок",
        "content_type": "text",
        "text_uk": "Повний логістичний супровід на всіх етапах роботи з вантажем",
        "text_en": "Full logistics support at every cargo stage",
        "sort_order": 20,
    },
    ("home", "hero_lead"): {
        "label": "Підзаголовок",
        "content_type": "text",
        "text_uk": "Власні склади, митне оформлення, страхування вантажу й авто.",
        "text_en": "Own warehouses, customs clearance, cargo and vehicle insurance.",
        "sort_order": 30,
    },
    ("home", "hero_fact_year"): {
        "label": "Факт (рік)",
        "content_type": "text",
        "text_uk": "З 2007 року",
        "text_en": "Since 2007",
        "sort_order": 40,
    },
    ("home", "hero_fact_rest"): {
        "label": "Факт (продовження)",
        "content_type": "text",
        "text_uk": "на ринку міжнародних перевезень",
        "text_en": "on the international freight market",
        "sort_order": 50,
    },
    ("home", "hero_form_title"): {
        "label": "Заголовок форми",
        "content_type": "text",
        "text_uk": "Розрахуємо маршрут за 15 хвилин",
        "text_en": "We'll quote your lane in 15 minutes",
        "sort_order": 60,
    },
    # —— Home / Scenarios ——
    ("home", "scenarios_section_visible"): {
        "label": "Показувати блок «Три сценарії»",
        "content_type": "text",
        "text_uk": "1",
        "text_en": "1",
        "sort_order": 100,
    },
    ("home", "scenarios_eyebrow"): {
        "label": "Eyebrow",
        "content_type": "text",
        "text_uk": "Як ми можемо допомогти",
        "text_en": "How we can help",
        "sort_order": 110,
    },
    ("home", "scenarios_title"): {
        "label": "Заголовок секції",
        "content_type": "text",
        "text_uk": "Три сценарії перевезення",
        "text_en": "Three shipping scenarios",
        "sort_order": 120,
    },
    ("home", "scenarios_lead"): {
        "label": "Лід секції",
        "content_type": "text",
        "text_uk": "Обираєте формат — решту бере на себе команда ПРИВАТ-ТРАНС.",
        "text_en": "Choose the format — Privat-Trans handles the rest.",
        "sort_order": 130,
    },
    ("home", "scenarios_cta"): {
        "label": "Текст кнопки карток",
        "content_type": "text",
        "text_uk": "Детальніше",
        "text_en": "Learn more",
        "sort_order": 140,
    },
    ("home", "scenario_1_title"): {
        "label": "Картка 1 — заголовок",
        "content_type": "text",
        "text_uk": "Збірний вантаж (LTL)\nвід 10кг",
        "text_en": "Groupage (LTL)\nfrom 10 kg",
        "sort_order": 150,
    },
    ("home", "scenario_1_text"): {
        "label": "Картка 1 — текст",
        "content_type": "text",
        "text_uk": "Не чекаєте на повну фуру — консолідуємо ваш вантаж з іншими відправленнями.",
        "text_en": (
            "No need to wait for a full truck — we consolidate your freight with other shipments. "
            "Regular weekly departures from Europe and Asia. "
            "You pay only for the pallet space your goods occupy — no charge for empty truck capacity."
        ),
        "sort_order": 160,
    },
    ("home", "scenario_1_slug"): {
        "label": "Картка 1 — slug послуги",
        "content_type": "text",
        "text_uk": "zbirni-vid-10-kg",
        "text_en": "zbirni-vid-10-kg",
        "sort_order": 170,
    },
    ("home", "scenario_2_title"): {
        "label": "Картка 2 — заголовок",
        "content_type": "text",
        "text_uk": "Повне авто (FTL)\nдо 23 тонн",
        "text_en": "Full truck (FTL)\nup to 23 tonnes",
        "sort_order": 180,
    },
    ("home", "scenario_2_text"): {
        "label": "Картка 2 — текст",
        "content_type": "text",
        "text_uk": "FTL перевезення: тенти(86-120 м2), рефрижератори, ізотерми, небезпечні (ADR) та негабаритні вантажі.",
        "text_en": "FTL: tautliners (86–120 m²), reefers, isotherms, ADR and oversized cargo.",
        "sort_order": 190,
    },
    ("home", "scenario_2_slug"): {
        "label": "Картка 2 — slug послуги",
        "content_type": "text",
        "text_uk": "povne-avto-ftl",
        "text_en": "povne-avto-ftl",
        "sort_order": 200,
    },
    ("home", "scenario_3_title"): {
        "label": "Картка 3 — заголовок",
        "content_type": "text",
        "text_uk": "Під ключ: склади перетримки та консолідації в Європі",
        "text_en": "Turnkey: storage and consolidation warehouses in Europe",
        "sort_order": 210,
    },
    ("home", "scenario_3_text"): {
        "label": "Картка 3 — текст",
        "content_type": "text",
        "text_uk": "Відповідальне зберігання, перетарка, маркування, палетування та пакування ваших товарів на європейських складах.",
        "text_en": "Responsible storage, re-packing, labeling, palletizing and packaging of your goods at European warehouses.",
        "sort_order": 220,
    },
    ("home", "scenario_3_slug"): {
        "label": "Картка 3 — slug послуги",
        "content_type": "text",
        "text_uk": "vlasni-sklady",
        "text_en": "vlasni-sklady",
        "sort_order": 230,
    },
    # —— About ——
    ("about", "about_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": "Повний логістичний супровід на всіх етапах роботи з вантажем. З 2007 року на ринку міжнародних перевезень.",
        "text_en": "Full logistics support at every cargo stage. On the international freight market since 2007.",
        "sort_order": 10,
    },
    ("about", "about_infra_title"): {
        "label": "Інфраструктура — заголовок",
        "content_type": "text",
        "text_uk": "Своя інфраструктура",
        "text_en": "Own infrastructure",
        "sort_order": 20,
    },
    ("about", "about_infra_body"): {
        "label": "Інфраструктура — текст",
        "content_type": "text",
        "text_uk": (
            "<ul><li>Власні склади перетримки та консолідації в Європі</li>"
            "<li>Митниця: Т1, Т2, EX1 і повне очищення</li>"
            "<li>Власний автопарк і партнерський флот</li></ul>"
        ),
        "text_en": (
            "<ul><li>Own staging and consolidation warehouses in Europe</li>"
            "<li>Customs: T1, T2, EX1 and full clearance</li>"
            "<li>Own fleet and partner fleet</li></ul>"
        ),
        "sort_order": 30,
    },
    ("about", "about_geo_title"): {
        "label": "Географія — заголовок",
        "content_type": "text",
        "text_uk": "Географія",
        "text_en": "Geography",
        "sort_order": 40,
    },
    ("about", "about_geo_body"): {
        "label": "Географія — текст",
        "content_type": "text",
        "text_uk": "Логістичні коридори, які ми контролюємо — Європа та Азія.",
        "text_en": "Logistics corridors we control — Europe and Asia.",
        "sort_order": 50,
    },
    ("about", "about_gallery_eyebrow"): {
        "label": "Галерея — eyebrow",
        "content_type": "text",
        "text_uk": "Наші роботи",
        "text_en": "Our work",
        "sort_order": 52,
    },
    ("about", "about_gallery_title"): {
        "label": "Галерея — заголовок",
        "content_type": "text",
        "text_uk": "Галерея робіт",
        "text_en": "Work gallery",
        "sort_order": 53,
    },
    ("about", "about_career_title"): {
        "label": "Вакансії — заголовок",
        "content_type": "text",
        "text_uk": "Відкриті вакансії",
        "text_en": "Open positions",
        "sort_order": 60,
    },
    # —— Contacts ——
    ("contacts", "contacts_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": "",
        "text_en": "",
        "sort_order": 10,
    },
    # —— Privacy ——
    ("privacy", "privacy_body"): {
        "label": "Текст політики",
        "content_type": "text",
        "text_uk": (
            "<h2>Які дані збираємо</h2>"
            "<p>Ім’я, телефон, email та параметри маршруту з форм заявки. "
            "Дані потрібні, щоб відповісти на запит.</p>"
            "<h2>Як використовуємо</h2>"
            "<p>Заявки зберігаються в адмінці, за потреби надсилаються на email, "
            "у Telegram або CRM Замовника.</p>"
            "<h2>Контакт</h2>"
        ),
        "text_en": (
            "<h2>What we collect</h2>"
            "<p>Name, phone, email and route details from inquiry forms. "
            "Needed to respond to your request.</p>"
            "<h2>How we use data</h2>"
            "<p>Leads are stored in admin and may be sent by email, Telegram or CRM.</p>"
            "<h2>Contact</h2>"
        ),
        "sort_order": 10,
    },
    # —— Services list ——
    ("services", "services_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": "",
        "text_en": "",
        "sort_order": 10,
    },
    # —— FAQ ——
    ("faq", "faq_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": "",
        "text_en": "",
        "sort_order": 10,
    },
    # —— Calculator ——
    ("calculator", "calculator_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": "Мок-формула для демонстрації. Не є офертою і не тарифною сіткою Замовника.",
        "text_en": "Demo formula only. Not an offer and not the client's tariff grid.",
        "sort_order": 10,
    }
}
BLOCK_DEFAULTS.update(FLEET_BLOCK_DEFAULTS)
BLOCK_DEFAULTS.update(HOME_BODY_BLOCK_DEFAULTS)

INLINE_KEYS = frozenset(
    {
        "hero_badge",
        "hero_badge_rest",
        "hero_fact_year",
        "hero_fact_rest",
        "hero_form_title",
        "hero_cta_call",
        "hero_cta_telegram",
        "hero_submit",
        "about_infra_title",
        "about_geo_title",
        "about_career_title",
        "about_gallery_eyebrow",
        "about_gallery_title",
        "scenarios_eyebrow",
        "scenarios_cta",
        "scenario_1_title",
        "scenario_1_slug",
        "scenario_2_title",
        "scenario_2_slug",
        "scenario_3_title",
        "scenario_3_slug",
    }
) | FLEET_INLINE_KEYS

MULTILINE_KEYS = frozenset(
    {
        "hero_title",
        "hero_lead",
        "about_lead",
        "about_geo_body",
        "contacts_lead",
        "services_lead",
        "faq_lead",
        "calculator_lead",
        "scenarios_title",
        "scenarios_lead",
        "scenario_1_text",
        "scenario_2_text",
        "scenario_3_text",
    }
) | FLEET_MULTILINE_KEYS

TINYMCE_KEYS = frozenset(
    {
        "about_infra_body",
        "about_geo_body",
        "privacy_body",
        "scenarios_lead",
        "scenario_1_text",
        "scenario_2_text",
        "scenario_3_text",
    }
) | FLEET_TINYMCE_KEYS


def is_visibility_key(key: str) -> bool:
    return key.endswith("_visible")


def uses_tinymce(key: str) -> bool:
    """Усі CMS-поля з редактором, крім Hero, visibility і slug."""
    if is_visibility_key(key) or key.endswith("_slug"):
        return False
    if key.startswith("hero_"):
        return False
    return True
