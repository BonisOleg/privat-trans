from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ""
    sidebar_icon: str = "edit_note"
    preview_url: str = "/"
    description: str = ""
    visibility_key: str = ""
    admin_model_name: str = ""


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug="hero",
        page_slug="home",
        title="Головна — Hero",
        sidebar_title="Головна — Hero",
        sidebar_icon="image",
        preview_url="/",
        description="Тексти першого екрану головної сторінки.",
        visibility_key="hero_section_visible",
        admin_model_name="homeherosettings",
        blocks=(
            ("home", "hero_badge"),
            ("home", "hero_title"),
            ("home", "hero_lead"),
            ("home", "hero_fact_year"),
            ("home", "hero_fact_rest"),
            ("home", "hero_form_title"),
        ),
    ),
    ContentSection(
        slug="scenarios",
        page_slug="home",
        title="Головна — Три сценарії",
        sidebar_title="Головна — Сценарії",
        sidebar_icon="view_agenda",
        preview_url="/",
        description=(
            "Блок «Три сценарії перевезення». "
            "У полях slug — slug послуги з розділу «Послуги» (напр. zbirni-vid-10-kg)."
        ),
        visibility_key="scenarios_section_visible",
        admin_model_name="homescenariossettings",
        blocks=(
            ("home", "scenarios_eyebrow"),
            ("home", "scenarios_title"),
            ("home", "scenarios_lead"),
            ("home", "scenarios_cta"),
            ("home", "scenario_1_title"),
            ("home", "scenario_1_text"),
            ("home", "scenario_1_slug"),
            ("home", "scenario_2_title"),
            ("home", "scenario_2_text"),
            ("home", "scenario_2_slug"),
            ("home", "scenario_3_title"),
            ("home", "scenario_3_text"),
            ("home", "scenario_3_slug"),
        ),
    ),
    ContentSection(
        slug="page",
        page_slug="about",
        title="Про нас",
        sidebar_title="Про нас",
        sidebar_icon="info",
        preview_url="/about/",
        description="Тексти сторінки «Про нас».",
        admin_model_name="aboutpagesettings",
        blocks=(
            ("about", "about_lead"),
            ("about", "about_infra_title"),
            ("about", "about_infra_body"),
            ("about", "about_geo_title"),
            ("about", "about_geo_body"),
            ("about", "about_career_title"),
        ),
    ),
    ContentSection(
        slug="page",
        page_slug="contacts",
        title="Контакти",
        sidebar_title="Контакти",
        sidebar_icon="call",
        preview_url="/contacts/",
        description="Додатковий лід на сторінці контактів (телефон/адреса — у Налаштуваннях).",
        admin_model_name="contactspagesettings",
        blocks=(("contacts", "contacts_lead"),),
    ),
    ContentSection(
        slug="page",
        page_slug="privacy",
        title="Політика конфіденційності",
        sidebar_title="Політика",
        sidebar_icon="policy",
        preview_url="/privacy/",
        description="Текст політики конфіденційності.",
        admin_model_name="privacypagesettings",
        blocks=(("privacy", "privacy_body"),),
    ),
    ContentSection(
        slug="page",
        page_slug="services",
        title="Послуги — сторінка",
        sidebar_title="Послуги (сторінка)",
        sidebar_icon="view_list",
        preview_url="/services/",
        description="Лід списку послуг. Картки послуг — у розділі «Послуги».",
        admin_model_name="servicespagesettings",
        blocks=(("services", "services_lead"),),
    ),
    ContentSection(
        slug="page",
        page_slug="faq",
        title="FAQ — сторінка",
        sidebar_title="FAQ (сторінка)",
        sidebar_icon="quiz",
        preview_url="/faq/",
        description="Лід сторінки FAQ. Питання — у розділі «FAQ».",
        admin_model_name="faqpagesettings",
        blocks=(("faq", "faq_lead"),),
    ),
    ContentSection(
        slug="page",
        page_slug="calculator",
        title="Калькулятор",
        sidebar_title="Калькулятор",
        sidebar_icon="calculate",
        preview_url="/calculator/",
        description="Лід сторінки калькулятора.",
        admin_model_name="calculatorpagesettings",
        blocks=(("calculator", "calculator_lead"),),
    ),
)


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def get_section_by_admin_model(admin_model_name: str) -> ContentSection | None:
    name = admin_model_name.lower()
    for section in CONTENT_SECTIONS:
        if section.admin_model_name == name:
            return section
    return None
