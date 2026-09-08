"""CMS defaults for homepage body sections and shared site CTAs (keeps block_defaults.py under 500 lines)."""

from __future__ import annotations


def _t(label: str, uk: str, en: str, sort_order: int) -> dict:
    return {
        "label": label,
        "content_type": "text",
        "text_uk": uk,
        "text_en": en,
        "sort_order": sort_order,
    }


HOME_BODY_BLOCK_DEFAULTS: dict[tuple[str, str], dict] = {
    # —— Site / Footer & global CTAs ——
    ("site", "footer_lead"): _t(
        "Футер — опис компанії",
        "20 років на ринку міжнародних перевезень. Повний логістичний супровід на всіх етапах роботи з вантажем.",
        "20 years on the international freight market. Full logistics support at every cargo stage.",
        10,
    ),
    ("site", "cta_lead"): _t("CTA — заявка", "Залишити заявку", "Request a quote", 11),
    ("site", "cta_call"): _t("CTA — дзвінок", "Зателефонувати", "Call us", 12),
    ("site", "cta_telegram"): _t("CTA — Telegram", "Написати в Telegram", "Message on Telegram", 13),
    ("site", "lead_eyebrow"): _t("Форма заявки — eyebrow", "Заявка", "Inquiry", 14),
    ("site", "lead_title"): _t("Форма заявки — заголовок", "Залишити заявку", "Request a quote", 15),
    ("site", "lead_lead"): _t(
        "Форма заявки — лід",
        "Ім'я, телефон і маршрут — розрахунок за 15 хвилин.",
        "Name, phone and route — we'll quote within 15 minutes.",
        16,
    ),
    ("site", "lead_submit"): _t("Форма заявки — кнопка", "Надіслати заявку", "Send inquiry", 17),
    ("site", "about_resume_cta"): _t("Вакансії — надіслати резюме", "Надіслати резюме", "Send résumé", 18),
    # —— Calculator extras ——
    ("calculator", "calculator_empty"): _t(
        "Калькулятор — порожній стан",
        "Заповніть форму — покажемо діапазон у €.",
        "Fill in the form — we'll show a range in €.",
        20,
    ),
    ("calculator", "calculator_result_label"): _t("Калькулятор — підпис результату", "Орієнтовно", "Estimate", 21),
    ("calculator", "calculator_disclaimer"): _t(
        "Калькулятор — дисклеймер",
        "Це не фінальна ціна. Менеджер підтвердить тариф.",
        "Not a final price. A manager will confirm the rate.",
        22,
    ),
    ("calculator", "calculator_submit"): _t(
        "Калькулятор — кнопка розрахунку",
        "Розрахувати орієнтовно",
        "Calculate estimate",
        23,
    ),
    ("calculator", "calculator_cta_lead"): _t("Калькулятор — CTA заявка", "Залишити заявку", "Request a quote", 24),
    # —— Home / Hero CTAs ——
    ("home", "hero_cta_call"): _t("Hero — зателефонувати", "Зателефонувати", "Call us", 70),
    ("home", "hero_cta_telegram"): _t("Hero — Telegram", "Написати в Telegram", "Message on Telegram", 71),
    ("home", "hero_submit"): _t("Hero — кнопка форми", "Отримати розрахунок", "Get a quote", 72),
    # —— About / Stats ——
    ("about", "about_stat_1_value"): _t("Статистика 1 — значення", "2007", "2007", 70),
    ("about", "about_stat_1_label"): _t("Статистика 1 — підпис", "старт на ринку", "market entry", 71),
    ("about", "about_stat_2_value"): _t("Статистика 2 — значення", "20 р", "20 yrs", 72),
    ("about", "about_stat_2_label"): _t("Статистика 2 — підпис", "на ринку перевезень", "on the freight market", 73),
    ("about", "about_stat_3_value"): _t("Статистика 3 — значення", "2", "2", 74),
    ("about", "about_stat_3_label"): _t("Статистика 3 — підпис", "напрямки: Європа і Азія", "lanes: Europe and Asia", 75),
    ("about", "about_stat_4_value"): _t("Статистика 4 — значення", "23 т", "23 t", 76),
    ("about", "about_stat_4_label"): _t("Статистика 4 — підпис", "повне авто", "full truck load", 77),
    # —— Home / Geography & regions ——
    ("home", "regions_eyebrow"): _t("Географія — eyebrow", "Географія", "Geography", 300),
    ("home", "regions_title"): _t("Географія — заголовок", "Два напрямки — Європа та Азія", "Two lanes — Europe and Asia", 301),
    ("home", "region_eu_kicker"): _t("Європа — kicker", "EU", "EU", 310),
    ("home", "region_eu_title"): _t("Європа — заголовок", "Європа", "Europe", 311),
    ("home", "region_eu_text"): _t(
        "Європа — текст",
        "Регулярні рейси між Україною та країнами ЄС — тенти, повні авто та збірні вантажі.",
        "Regular lanes between Ukraine and EU countries — curtain siders, full trucks and groupage freight.",
        312,
    ),
    ("home", "region_eu_chips"): _t(
        "Європа — країни (HTML)",
        "<ul><li>Польща</li><li>Німеччина</li><li>Італія</li><li>Чехія</li></ul>",
        "<ul><li>Poland</li><li>Germany</li><li>Italy</li><li>Czechia</li></ul>",
        313,
    ),
    ("home", "region_as_kicker"): _t("Азія — kicker", "AS", "AS", 320),
    ("home", "region_as_title"): _t("Азія — заголовок", "Азія", "Asia", 321),
    ("home", "region_as_text"): _t(
        "Азія — текст",
        "Автомобільні та мультимодальні маршрути через Туреччину, Кавказ і Центральну Азію.",
        "Road and multimodal routes via Turkey, the Caucasus and Central Asia.",
        322,
    ),
    ("home", "region_as_chips"): _t(
        "Азія — країни (HTML)",
        "<ul><li>Туреччина</li><li>Грузія</li><li>Казахстан</li><li>Узбекистан</li></ul>",
        "<ul><li>Turkey</li><li>Georgia</li><li>Kazakhstan</li><li>Uzbekistan</li></ul>",
        323,
    ),
    # —— Home / Corridor bridge ——
    ("home", "corridor_eyebrow"): _t("Коридор — eyebrow", "Зв'язок напрямків", "Connecting lanes", 400),
    ("home", "corridor_title"): _t(
        "Коридор — заголовок",
        "Від географії — до контрольованих коридорів",
        "From geography to controlled corridors",
        401,
    ),
    ("home", "corridor_lead"): _t(
        "Коридор — лід",
        "Європа та Азія — це не просто регіони на карті. Це регулярні маршрути з єдиним супроводом вантажу на всьому шляху.",
        "Europe and Asia are not just regions on a map. They are regular lanes with unified cargo support end to end.",
        402,
    ),
    ("home", "corridor_fact_1_value"): _t("Коридор — факт 1 значення", "2007", "2007", 410),
    ("home", "corridor_fact_1_label"): _t("Коридор — факт 1 підпис", "на ринку перевезень", "on the freight market", 411),
    ("home", "corridor_fact_2_value"): _t("Коридор — факт 2 значення", "10 кг – 23 т", "10 kg – 23 t", 412),
    ("home", "corridor_fact_2_label"): _t("Коридор — факт 2 підпис", "збірні та повні авто", "groupage and full trucks", 413),
    ("home", "corridor_fact_3_value"): _t("Коридор — факт 3 значення", "EU ↔ AS", "EU ↔ AS", 414),
    ("home", "corridor_fact_3_label"): _t("Коридор — факт 3 підпис", "два напрямки під контролем", "two lanes under our control", 415),
    # —— Home / Routes ——
    ("home", "routes_eyebrow"): _t("Маршрути — eyebrow", "Маршрути", "Routes", 500),
    ("home", "routes_title"): _t("Маршрути — заголовок", "Логістичні коридори, які ми контролюємо", "Logistics corridors we control", 501),
    ("home", "routes_lead"): _t(
        "Маршрути — лід",
        "Регулярні маршрути в обох напрямках із власним автопарком і партнерською мережею.",
        "Regular lanes both ways with our own fleet and partner network.",
        502,
    ),
    ("home", "routes_filter_all"): _t("Маршрути — фільтр «Усі»", "Усі", "All", 510),
    ("home", "routes_filter_europe"): _t("Маршрути — фільтр «Європа»", "Європа", "Europe", 511),
    ("home", "routes_filter_asia"): _t("Маршрути — фільтр «Азія»", "Азія", "Asia", 512),
    # —— Home / Services teaser ——
    ("home", "services_home_eyebrow"): _t("Послуги на головній — eyebrow", "Що ми перевозимо", "What we ship", 600),
    ("home", "services_home_title"): _t("Послуги на головній — заголовок", "Вісім послуг під ваш вантаж", "Eight services for your cargo", 601),
    ("home", "services_home_cta"): _t("Послуги на головній — CTA картки", "Детальніше", "Learn more", 602),
    # —— Home / Fleet teaser ——
    ("home", "fleet_home_eyebrow"): _t("Автопарк на головній — eyebrow", "Автопарк та можливості", "Fleet & capacity", 700),
    ("home", "fleet_home_title"): _t("Автопарк на головній — заголовок", "Наш автопарк", "Our fleet", 701),
    ("home", "fleet_home_lead"): _t(
        "Автопарк на головній — лід",
        "Завдяки гнучкому поєднанню власного автопарку та перевіреного партнерського флоту, ми забезпечуємо безперебійну логістику та закриваємо будь-які об'єми перевезень навіть у пікові сезони.",
        "A flexible mix of our own fleet and a vetted partner network keeps logistics running and covers any volume — even in peak seasons.",
        702,
    ),
    ("home", "fleet_home_cta"): _t("Автопарк на головній — CTA", "Детальніше про автопарк", "More about the fleet", 703),
    ("home", "fleet_home_fact_1_value"): _t("Автопарк на головній — факт 1 значення", "10 кг – 23 т", "10 kg – 23 t", 710),
    ("home", "fleet_home_fact_1_label"): _t("Автопарк на головній — факт 1 підпис", "Від збірних до повного авто", "From groupage to full truck", 711),
    ("home", "fleet_home_fact_2_value"): _t("Автопарк на головній — факт 2 значення", "Тент · реф", "Curtain · reefer", 712),
    ("home", "fleet_home_fact_2_label"): _t("Автопарк на головній — факт 2 підпис", "Кузови під різні вантажі", "Bodies for different cargo types", 713),
    ("home", "fleet_home_fact_3_value"): _t("Автопарк на головній — факт 3 значення", "Власний + партнери", "Own + partners", 714),
    ("home", "fleet_home_fact_3_label"): _t("Автопарк на головній — факт 3 підпис", "Гнучкий флот у пікові сезони", "Flexible capacity in peak seasons", 715),
    # —— Home / Advantages ——
    ("home", "advantages_title"): _t("Переваги — заголовок", "Чому з нами", "Why work with us", 800),
    ("home", "advantage_1_title"): _t("Перевага 1 — заголовок", "Підтримка 24/7", "24/7 support", 810),
    ("home", "advantage_1_text"): _t(
        "Перевага 1 — текст",
        "Постійний зв'язок та моніторинг вантажу на кожному етапі.",
        "Always-on contact and cargo monitoring at every stage.",
        811,
    ),
    ("home", "advantage_2_title"): _t("Перевага 2 — заголовок", "Досвідчені менеджери", "Experienced managers", 812),
    ("home", "advantage_2_text"): _t(
        "Перевага 2 — текст",
        "Професіоналізм та персональний підхід до кожного маршруту.",
        "Professionalism and a personal approach to every lane.",
        813,
    ),
    ("home", "advantage_3_title"): _t("Перевага 3 — заголовок", "Обов'язкове страхування", "Mandatory insurance", 814),
    ("home", "advantage_3_text"): _t(
        "Перевага 3 — текст",
        "Повний фінансовий та юридичний захист вашого майна.",
        "Full financial and legal protection for your goods.",
        815,
    ),
    # —— Home / Process ——
    ("home", "process_eyebrow"): _t("Процес — eyebrow", "Маршрут угоди", "Deal journey", 900),
    ("home", "process_title"): _t("Процес — заголовок", "Як це відбувається", "How it works", 901),
    ("home", "process_1_title"): _t("Крок 1 — заголовок", "Заявка", "Inquiry", 910),
    ("home", "process_1_text"): _t("Крок 1 — текст", "Маршрут і тип вантажу.", "Route and cargo type.", 911),
    ("home", "process_2_title"): _t("Крок 2 — заголовок", "Розрахунок", "Quote", 912),
    ("home", "process_2_text"): _t("Крок 2 — текст", "Орієнтовна вартість і слот.", "Estimated cost and slot.", 913),
    ("home", "process_3_title"): _t("Крок 3 — заголовок", "Документи", "Documents", 914),
    ("home", "process_3_text"): _t("Крок 3 — текст", "Митниця Т1/Т2, EX1.", "Customs T1/T2, EX1.", 915),
    ("home", "process_4_title"): _t("Крок 4 — заголовок", "Рейс", "Trip", 916),
    ("home", "process_4_text"): _t("Крок 4 — текст", "Моніторинг 24/7.", "24/7 monitoring.", 917),
    # —— Home / Calculator teaser ——
    ("home", "calc_teaser_eyebrow"): _t("Калькулятор-тизер — eyebrow", "Калькулятор", "Calculator", 1000),
    ("home", "calc_teaser_title"): _t("Калькулятор-тизер — заголовок", "Орієнтовний розрахунок", "Estimated quote", 1001),
    ("home", "calc_teaser_item_1"): _t("Калькулятор-тизер — пункт 1", "Звідки / куди, вага, тип кузова", "From / to, weight, body type", 1010),
    ("home", "calc_teaser_item_2"): _t("Калькулятор-тизер — пункт 2", "Результат — діапазон у євро, не оферта", "Result is a euro range, not an offer", 1011),
    ("home", "calc_teaser_cta"): _t("Калькулятор-тизер — CTA", "Відкрити калькулятор", "Open calculator", 1012),
    ("home", "calc_teaser_panel_label"): _t("Калькулятор-тизер — підпис панелі", "Приклад", "Example", 1020),
    ("home", "calc_teaser_route"): _t("Калькулятор-тизер — маршрут", "Київ → Warsaw", "Kyiv → Warsaw", 1021),
    ("home", "calc_teaser_meta"): _t("Калькулятор-тизер — параметри", "Збірний · ~1.2 т · тент", "Groupage · ~1.2 t · curtain", 1022),
    ("home", "calc_teaser_from"): _t("Калькулятор-тизер — від (€)", "420", "420", 1023),
    ("home", "calc_teaser_to"): _t("Калькулятор-тизер — до (€)", "560", "560", 1024),
    ("home", "calc_teaser_note"): _t(
        "Калькулятор-тизер — примітка",
        "Це не фінальна ціна. Менеджер підтвердить тариф.",
        "Not a final price. A manager will confirm the rate.",
        1025,
    ),
    # —— Home / Social blocks ——
    ("home", "faq_home_title"): _t("FAQ на головній — заголовок", "FAQ", "FAQ", 1100),
    ("home", "faq_home_cta"): _t("FAQ на головній — CTA", "Усі питання", "All questions", 1101),
    ("home", "reviews_title"): _t("Відгуки — заголовок", "Відгуки", "Reviews", 1110),
    ("home", "partners_title"): _t("Партнери — заголовок", "Партнери", "Partners", 1120),
    ("home", "career_kicker"): _t("Кар'єра — kicker", "Кар'єра", "Careers", 1130),
    ("home", "career_title"): _t("Кар'єра — заголовок", "Приєднуйтесь до команди", "Join the team", 1131),
    ("home", "career_text"): _t(
        "Кар'єра — текст",
        "Шукаємо менеджерів логістики та спеціалістів митного оформлення.",
        "We're hiring logistics managers and customs specialists.",
        1132,
    ),
    ("home", "career_cta"): _t("Кар'єра — CTA", "Вакансії", "Open roles", 1133),
}
