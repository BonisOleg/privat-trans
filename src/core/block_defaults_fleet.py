"""CMS defaults for the Fleet page (keeps block_defaults.py under 500 lines)."""

from __future__ import annotations

FLEET_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    ("fleet", "fleet_lead"): {
        "label": "Лід під H1",
        "content_type": "text",
        "text_uk": (
            "Завдяки гнучкому поєднанню власного автопарку та перевіреного партнерського флоту "
            "закриваємо будь-які об’єми перевезень навіть у пікові сезони."
        ),
        "text_en": (
            "A flexible mix of our own fleet and a vetted partner network covers any volume — "
            "even in peak seasons."
        ),
        "sort_order": 10,
    },
    ("fleet", "fleet_fact_1_value"): {
        "label": "Факт 1 — значення",
        "content_type": "text",
        "text_uk": "10 кг – 23 т",
        "text_en": "10 kg – 23 t",
        "sort_order": 20,
    },
    ("fleet", "fleet_fact_1_label"): {
        "label": "Факт 1 — підпис",
        "content_type": "text",
        "text_uk": "Від збірних до повного авто",
        "text_en": "From groupage to full truck",
        "sort_order": 21,
    },
    ("fleet", "fleet_fact_2_value"): {
        "label": "Факт 2 — значення",
        "content_type": "text",
        "text_uk": "Тент · реф · ізотерм",
        "text_en": "Curtain · reefer · isotherm",
        "sort_order": 22,
    },
    ("fleet", "fleet_fact_2_label"): {
        "label": "Факт 2 — підпис",
        "content_type": "text",
        "text_uk": "Кузови під різні вантажі",
        "text_en": "Bodies for different cargo types",
        "sort_order": 23,
    },
    ("fleet", "fleet_fact_3_value"): {
        "label": "Факт 3 — значення",
        "content_type": "text",
        "text_uk": "Власний + партнери",
        "text_en": "Own + partners",
        "sort_order": 24,
    },
    ("fleet", "fleet_fact_3_label"): {
        "label": "Факт 3 — підпис",
        "content_type": "text",
        "text_uk": "Гнучкий флот у пікові сезони",
        "text_en": "Flexible capacity in peak seasons",
        "sort_order": 25,
    },
    ("fleet", "fleet_bodies_eyebrow"): {
        "label": "Типи кузовів — eyebrow",
        "content_type": "text",
        "text_uk": "Техніка",
        "text_en": "Equipment",
        "sort_order": 30,
    },
    ("fleet", "fleet_bodies_title"): {
        "label": "Типи кузовів — заголовок",
        "content_type": "text",
        "text_uk": "Кузови під ваш вантаж",
        "text_en": "Bodies matched to your cargo",
        "sort_order": 31,
    },
    ("fleet", "fleet_bodies_lead"): {
        "label": "Типи кузовів — лід",
        "content_type": "text",
        "text_uk": "Підбираємо тип кузова під характер вантажу, сезон і маршрут.",
        "text_en": "We match body type to cargo, season and lane.",
        "sort_order": 32,
    },
    ("fleet", "fleet_body_1_title"): {
        "label": "Кузов 1 — заголовок",
        "content_type": "text",
        "text_uk": "Тент (86–120 м²)",
        "text_en": "Curtain sider (86–120 m²)",
        "sort_order": 40,
    },
    ("fleet", "fleet_body_1_text"): {
        "label": "Кузов 1 — текст",
        "content_type": "text",
        "text_uk": "Загальні комерційні вантажі, палети, обладнання. Бічне та верхнє завантаження.",
        "text_en": "General cargo, pallets, equipment. Side and top loading.",
        "sort_order": 41,
    },
    ("fleet", "fleet_body_2_title"): {
        "label": "Кузов 2 — заголовок",
        "content_type": "text",
        "text_uk": "Рефрижератор",
        "text_en": "Reefer",
        "sort_order": 42,
    },
    ("fleet", "fleet_body_2_text"): {
        "label": "Кузов 2 — текст",
        "content_type": "text",
        "text_uk": "Продукти, медикаменти та інші вантажі з температурним режимом на всьому маршруті.",
        "text_en": "Food, pharma and other temperature-controlled cargo end to end.",
        "sort_order": 43,
    },
    ("fleet", "fleet_body_3_title"): {
        "label": "Кузов 3 — заголовок",
        "content_type": "text",
        "text_uk": "Ізотерм",
        "text_en": "Isotherm",
        "sort_order": 44,
    },
    ("fleet", "fleet_body_3_text"): {
        "label": "Кузов 3 — текст",
        "content_type": "text",
        "text_uk": "Вантажі, чутливі до перепадів температури, без активного холоду.",
        "text_en": "Temperature-sensitive cargo without active cooling.",
        "sort_order": 45,
    },
    ("fleet", "fleet_capabilities_title"): {
        "label": "Можливості — заголовок",
        "content_type": "text",
        "text_uk": "Що закриваємо автопарком",
        "text_en": "What the fleet covers",
        "sort_order": 50,
    },
    ("fleet", "fleet_capabilities_body"): {
        "label": "Можливості — текст",
        "content_type": "text",
        "text_uk": (
            "<ul>"
            "<li>Збірні відправлення від 10 кг і повні авто до 23 т</li>"
            "<li>ADR / небезпечні та негабаритні вантажі за запитом</li>"
            "<li>Регулярні рейси Європа ↔ Україна ↔ Азія</li>"
            "<li>Моніторинг рейсу 24/7 і страхування вантажу</li>"
            "</ul>"
        ),
        "text_en": (
            "<ul>"
            "<li>Groupage from 10 kg and full trucks up to 23 t</li>"
            "<li>ADR / hazardous and oversized cargo on request</li>"
            "<li>Regular lanes Europe ↔ Ukraine ↔ Asia</li>"
            "<li>24/7 trip monitoring and cargo insurance</li>"
            "</ul>"
        ),
        "sort_order": 51,
    },
    ("fleet", "fleet_partners_title"): {
        "label": "Партнерський флот — заголовок",
        "content_type": "text",
        "text_uk": "Власний парк і партнерська мережа",
        "text_en": "Own fleet and partner network",
        "sort_order": 60,
    },
    ("fleet", "fleet_partners_body"): {
        "label": "Партнерський флот — текст",
        "content_type": "text",
        "text_uk": (
            "<p>Базовий обсяг закриваємо власним автопарком. У пікові сезони та на нестандартні "
            "маршрути підключаємо перевірених партнерів — з тими самими стандартами супроводу, "
            "документів і страхування.</p>"
        ),
        "text_en": (
            "<p>Core volume runs on our own fleet. In peak seasons and on non-standard lanes "
            "we bring in vetted partners — same standards for handling, documents and insurance.</p>"
        ),
        "sort_order": 61,
    },
    ("fleet", "fleet_faq_title"): {
        "label": "FAQ — заголовок",
        "content_type": "text",
        "text_uk": "Питання про автопарк",
        "text_en": "Fleet FAQ",
        "sort_order": 70,
    },
    ("fleet", "fleet_faq_1_q"): {
        "label": "FAQ 1 — питання",
        "content_type": "text",
        "text_uk": "Чи є власні авто, чи лише партнери?",
        "text_en": "Do you run own trucks or only partners?",
        "sort_order": 71,
    },
    ("fleet", "fleet_faq_1_a"): {
        "label": "FAQ 1 — відповідь",
        "content_type": "text",
        "text_uk": "Працюємо з власним автопарком і перевіреною партнерською мережею — залежно від обсягу, сезону та типу кузова.",
        "text_en": "We combine our own fleet with a vetted partner network — depending on volume, season and body type.",
        "sort_order": 72,
    },
    ("fleet", "fleet_faq_2_q"): {
        "label": "FAQ 2 — питання",
        "content_type": "text",
        "text_uk": "Який максимальний обсяг одного рейсу?",
        "text_en": "What is the max capacity per trip?",
        "sort_order": 73,
    },
    ("fleet", "fleet_faq_2_a"): {
        "label": "FAQ 2 — відповідь",
        "content_type": "text",
        "text_uk": "Повне авто — до 23 тонн / тенти 86–120 м². Для збірних — від 10 кг, ви платите за місце на палеті.",
        "text_en": "Full truck — up to 23 t / curtain 86–120 m². Groupage — from 10 kg; you pay for pallet space.",
        "sort_order": 74,
    },
    ("fleet", "fleet_faq_3_q"): {
        "label": "FAQ 3 — питання",
        "content_type": "text",
        "text_uk": "Чи потрібен температурний режим?",
        "text_en": "Do you offer temperature control?",
        "sort_order": 75,
    },
    ("fleet", "fleet_faq_3_a"): {
        "label": "FAQ 3 — відповідь",
        "content_type": "text",
        "text_uk": "Так — рефрижератори та ізотерми. Параметри режиму фіксуємо в заявці до виходу в рейс.",
        "text_en": "Yes — reefers and isotherms. Temperature params are locked in the booking before departure.",
        "sort_order": 76,
    },
}

FLEET_INLINE_KEYS = frozenset(
    {
        "fleet_fact_1_value",
        "fleet_fact_1_label",
        "fleet_fact_2_value",
        "fleet_fact_2_label",
        "fleet_fact_3_value",
        "fleet_fact_3_label",
        "fleet_bodies_eyebrow",
        "fleet_body_1_title",
        "fleet_body_2_title",
        "fleet_body_3_title",
        "fleet_capabilities_title",
        "fleet_partners_title",
        "fleet_faq_title",
        "fleet_faq_1_q",
        "fleet_faq_2_q",
        "fleet_faq_3_q",
    }
)

FLEET_MULTILINE_KEYS = frozenset(
    {
        "fleet_lead",
        "fleet_bodies_title",
        "fleet_bodies_lead",
        "fleet_body_1_text",
        "fleet_body_2_text",
        "fleet_body_3_text",
        "fleet_faq_1_a",
        "fleet_faq_2_a",
        "fleet_faq_3_a",
    }
)

FLEET_TINYMCE_KEYS = frozenset(
    {
        "fleet_capabilities_body",
        "fleet_partners_body",
    }
)
